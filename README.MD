![game_exe](https://github.com/ThisProgrammerG/Example_game_exe/assets/116992225/532aa847-e4ed-4eb0-8af1-a8b30eac2b9e)

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
