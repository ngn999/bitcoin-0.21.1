import lldb
import shlex
# push value
OP_PUSHDATA1 = 0x4c
OP_PUSHDATA2 = 0x4d
OP_PUSHDATA4 = 0x4e

def print_script(debugger, command, result, internal_dict):
    target = lldb.debugger.GetSelectedTarget()
    thread = target.GetProcess().GetSelectedThread()
    frame = thread.GetSelectedFrame()

    args = shlex.split(command)
    if len(args) == 0:
        print('please input a variable')
        return

    size = frame.EvaluateExpression("(int)%s.size()" % args[0])
    script_size = int(size.GetValue())

    pc = 0
    readable_script = []
    while pc < script_size:
        opcode = frame.EvaluateExpression("%s[%d]" % (args[0], pc))
        opcode.SetFormat(lldb.eFormatUnsigned)
        currentpc = pc
        pc += 1

        # push data
        if int(opcode.GetValue()) <= OP_PUSHDATA4:
            nsize = 0
            if int(opcode.GetValue()) < OP_PUSHDATA1:
                nsize = int(opcode.GetValue())
                readable_script.append("%d" % nsize)
            elif int(opcode.GetValue()) == OP_PUSHDATA1:
                pcvalue = frame.EvaluateExpression("%s[%d]" % (args[0], currentpc))
                pc += 1
                pcvalue.SetFormat(lldb.eBasicTypeUnsignedShort)
                nsize = int(pcvalue.GetValue())
                readable_script.append("OP_PUSHDATA1")
            elif int(opcode.GetValue()) == OP_PUSHDATA2:
                readable_script.append("OP_PUSHDATA2")
            elif int(opcode.GetValue()) == OP_PUSHDATA4:
                readable_script.append("OP_PUSHDATA4")
            # push data
            index = pc
            c = 0
            data_hex_string = "0x"
            while index < script_size and c < nsize:
                data = frame.EvaluateExpression("%s[%d]" % (args[0], index))
                data.SetFormat(lldb.eFormatHex)
                data_hex_string = data_hex_string + data.GetValue()[2:]
                index += 1
                c += 1
            pc += nsize
            readable_script.append(data_hex_string)
            continue
        else:
            # other opcode
            opname = frame.EvaluateExpression("GetOpName((opcodetype)%s[%d]).c_str()" % (args[0], currentpc))
            opname.SetFormat(lldb.eFormatCString)
            readable_script.append(opname.GetValue())
    print(' '.join(readable_script).replace('"', ''))


# And the initialization code to add your commands
def __lldb_init_module(debugger, internal_dict):
    # command script add syntax: `help command script add'
    debugger.HandleCommand('command script add --help "print bitcoin script" -f print_script.print_script pscript')
    print('The "pscript" python command has been installed and is ready for use.')
