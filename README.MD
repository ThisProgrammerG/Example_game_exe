Serves as an example for creating an executable with pygame and pyinstaller. Virtual environment is recommended.

Install requirements and run included spec file:
```
pyinstaller main.spec
```
Executable will be in the dist folder.

---
## First time running without a spec file
Run command: 
```
pyinstaller --onefile --noconsole main.py
```

Then add assets to spec file:
```python
assets = [
    ("./assets/", "assets"),
]

a = Analysis(
    ...
    datas=assets,
    ...

```
Again, run pyinstaller command:
```
pyinstaller main.spec
```