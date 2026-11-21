import subprocess

# Can we merge into an action or stop without endif diamond in new syntax?
tests = {}

# Test 1: what if endif is immediately followed by stop? Does PlantUML still draw the diamond?
tests['test_n1'] = '''@startuml
skinparam conditionStyle inside
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

# Test 2: What if we use 'end' instead of 'stop'?
tests['test_n2'] = '''@startuml
skinparam conditionStyle inside
start
:Giao diện;
if (Chọn?) then ([A])
  :Xử lý A;
else ([B])
  :Xử lý B;
endif
end
@enduml
'''

# Test 3: What if we detach one branch or both?
tests['test_n3'] = '''@startuml
skinparam conditionStyle inside
start
:Giao diện;
if (Chọn?) then ([A])
  :Xử lý A;
  stop
else ([B])
  :Xử lý B;
  stop
endif
@enduml
'''

# Test 4: Can we label stop? e.g. stop as my_stop?
tests['test_n4'] = '''@startuml
skinparam conditionStyle inside
start
:Giao diện;
if (Chọn?) then ([A])
  :Xử lý A;
  goto my_end
else ([B])
  :Xử lý B;
  goto my_end
endif
label my_end
stop
@enduml
'''

for name, code in tests.items():
    fname = f'{name}.puml'
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(code)
    res = subprocess.run(['java', '-jar', 'plantuml.jar', '-tpng', fname], capture_output=True, text=True)
    print(name, res.stdout, res.stderr)
