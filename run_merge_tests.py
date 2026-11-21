import subprocess

# Test various skinparams or syntaxes
tests = {}

# Test A: hide empty diamond?
tests['test_A'] = '''@startuml
skinparam conditionStyle inside
skinparam activityDiamond {
  BackgroundColor transparent
  BorderColor transparent
}
start
:Giao diện;
if (Chọn?) then ([A])
  :Xử lý A;
else ([B])
  :Xử lý B;
endif
stop
@enduml
'''

# Test B: can we use legacy syntax with conditionStyle inside?
tests['test_B'] = '''@startuml
skinparam conditionStyle inside
(*) --> "Giao diện"
if "Chọn?" then
  -->[A] "Xử lý A"
  --> (*)
else
  -->[B] "Xử lý B"
  --> (*)
endif
@enduml
'''

# Test C: What about goto / label in legacy syntax?
tests['test_C'] = '''@startuml
(*) --> "Giao diện"
--> ===B1===
--> "Xử lý A"
--> (*)
===B1=== --> "Xử lý B"
--> (*)
@enduml
'''

for name, code in tests.items():
    fname = f'{name}.puml'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(code)
    subprocess.run(['java', '-jar', 'plantuml.jar', '-tpng', fname])

print('Compiled tests')
