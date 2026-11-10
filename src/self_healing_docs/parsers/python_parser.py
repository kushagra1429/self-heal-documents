import ast
from self_healing_docs.models import SymbolChange

def signature(node):
    a = node.args
    positional = list(a.posonlyargs) + list(a.args)
    defaults = [None] * (len(positional)-len(a.defaults)) + list(a.defaults)
    parts = []
    for arg, default in zip(positional, defaults):
        item = arg.arg
        if arg.annotation: item += ": " + ast.unparse(arg.annotation)
        if default is not None: item += " = " + ast.unparse(default)
        parts.append(item)
    if a.vararg: parts.append("*" + a.vararg.arg)
    elif a.kwonlyargs: parts.append("*")
    for arg, default in zip(a.kwonlyargs, a.kw_defaults):
        parts.append(arg.arg + (" = " + ast.unparse(default) if default is not None else ""))
    if a.kwarg: parts.append("**" + a.kwarg.arg)
    result = "(" + ", ".join(parts) + ")"
    if node.returns: result += " -> " + ast.unparse(node.returns)
    return result

def extract(source):
    tree = ast.parse(source)
    found = {}
    def walk(body, prefix=""):
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_"):
                name = prefix + n.name
                found[name] = ("function", signature(n), ast.dump(n, include_attributes=False))
            elif isinstance(n, ast.ClassDef) and not n.name.startswith("_"):
                name = prefix + n.name
                found[name] = ("class", "class", ast.dump(n, include_attributes=False))
                walk(n.body, name + ".")
    walk(tree.body)
    return found

def classify(old_source, new_source):
    old = extract(old_source) if old_source is not None else {}
    new = extract(new_source) if new_source is not None else {}
    result = []
    for name in sorted(set(old) | set(new)):
        before, after = old.get(name), new.get(name)
        if before is None: kind = "added"
        elif after is None: kind = "removed"
        elif before[1] != after[1]: kind = "signature_changed"
        elif before[2] != after[2]: kind = "body_or_docstring_changed"
        else: continue
        result.append((name, kind, before, after))
    return result
