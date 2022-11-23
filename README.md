# Interpret

Transpiler of custom Go XML code into Python which is then executed

Sample of transpilled code

```python
@wrap_with_logging
def main():
    memory.create_temp_frame(instruction_createframe_1.run())
    memory.push_temp_frame(instruction_pushframe_2.run())
    memory.define_variable(instruction_defvar_3.run())
    memory.move_variable(instruction_move_4.run())
    memory.artihmetic_operation(instruction_add_11.run())
    memory.write_variable(instruction_write_7.run())
    memory.jump_if_hander(instruction_jumpifneq_8.run())
    while memory['help_var1'] != memory['help_var2']:
        memory.artihmetic_operation(instruction_add_11.run())
        memory.write_variable(instruction_write_7.run())
        memory.jump_if_hander(instruction_jumpifneq_8.run())
    memory.exit_handle(instruction_exit_9.run())
main()
```
