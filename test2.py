l = [{"a": "ex", "b": "ex2"}, {"a": "po", "b": "po2"}]

res = [d["a"] for d in l if d["b"] == "po2"]

print(res)