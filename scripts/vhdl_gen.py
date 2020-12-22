#################################################################################
# Copyright 2020 Ricardo F Tafas Jr

# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.
#################################################################################
import sys
import os

#TODO:
#process
#Functions
#Procedures
#Custom Custom
#Block

try:
    x = tabsize
except NameError:
    tabsize = 2

def indent(value):
    txt = ""
    if value > 0:
        for j in range(tabsize * value):
            txt = txt + " "
    return txt;

def VHDLenum(list):
    hdl_code = ""
    i = 0
    for j in list:
        i = i+1
        if (i == len(list)):
            hdl_code = hdl_code + list[j].code().replace(";","")
        else:
            hdl_code = hdl_code + list[j].code()
    return hdl_code

def dictCode(DictInput):
    hdl_code = ""
    for j in DictInput:
        hdl_code = hdl_code + DictInput[j].code()
    return hdl_code

class packageObj:
    def __init__(self, name, *args):
        self.source = "File Location Unknown."
        self.name = name
        if args:
            self.operator = args[0]
        else:
            self.operator = "all"

class packageList(dict):
    def add(self, name, *args):
        self[name] = packageObj(name)
        if args:
            self[name].operator = arg[0]

class libraryObj:
    def __init__(self, name, *args):
        self.name = name
        self.package = packageList()
    def code(self):
        hdl_code = ""
        hdl_code = hdl_code + indent(0) + ("library %s;\r\n" % self.name)
        for j in self.package:
            hdl_code = hdl_code + indent(1) + ("use %s.%s.%s;\r\n" % (self.name, j, self.package[j].operator))
        return hdl_code

class libraryList(dict):
    def add(self, name):
        self[name] = libraryObj(name)
    def code(self):
        return dictCode(self) + "\r\n"

class genericObj:
    def __init__(self, name, type, init_value):
        self.name = name
        self.init_value = init_value
        self.type = type
    def code(self):
        hdl_code = indent(2) + ("%s : %s := %s;\r\n" % (self.name, self.type, self.init_value))
        return hdl_code

class portObj:
    def __init__(self, name, direction, type):
        self.name = name
        self.direction = direction
        self.type = type
    def code(self):
        hdl_code = indent(2) + ("%s : %s %s;\r\n" % (self.name, self.direction, self.type))
        return hdl_code

class genericList(dict):
    def add(self, name, type, init):
        self[name] = genericObj(name,type,init)
    def code(self):
        return VHDLenum(self)

class portList(dict):
    def add(self, name, direction, type):
        self[name] = portObj(name, direction, type)
    def code(self):
        return VHDLenum(self)

class constantObj:
    def __init__(self, name, type, init):
        self.name = name
        self.type = type
        self.init = init
    def code(self):
        return indent(1) + "constant %s : %s := %s;\r\n" % (self.name, self.type, self.init)

class signalObj:
    def __init__(self, name, type, *args):
        self.name = name
        self.type = type
        if args:
            self.init = args[0]
        else:
            self.init = "undefined"
    def code(self):
        if self.init != "undefined":
            return indent(1) + ("signal %s : %s := %s;\r\n" % (self.name, self.type, self.init))
        else:
            return indent(1) + ("signal %s : %s;\r\n" % (self.name, self.type))

class variableObj:
    def __init__(self, name, type, *args):
        self.name = name
        self.type = type
        if args:
            self.init = args[0]
        else:
            self.init = "undefined"
    def code(self):
        if self.init != "undefined":
            return indent(1) + ("variable %s : %s := %s;\r\n" % (self.name, self.type, self.init))
        else:
            return indent(1) + ("variable %s : %s;\r\n" % (self.name, self.type))

class constantList(dict):
    def add(self,name,type,init):
        self[name] = constantObj(name,type,init)
    def code(self):
        return dictCode(self)

class signalList(dict):
    def add(self,name,type,*args):
        self[name] = signalObj(name,type,*args)
    def code(self):
        return dictCode(self)

class variableList(dict):
    def add(self,name,type,*args):
        self[name] = variableObj(name,type,*args)
    def code(self):
        return dictCode(self)

class genericCodeBlock:
    def __init__(self, indent):
        self.list = []
        self.indent = indent
    def add(self,text):
        self.list.append(text)
    def code(self):
        hdl_code = ""
        for j in self.list:
            hdl_code = hdl_code + indent(self.indent) + str(j) + "\r\n"
        return hdl_code

class functionObj:
    def __init__(self, name):
        self.name = name
        # todo: generic types here.
        self.generic = genericList()
        # function parameters in VHDL follow the same fashion as
        # generics on a portmap. name : type := init value;
        self.parameter = genericList()
        self.variable = variableList()
        self.functionBody = genericCodeBlock(1)
        self.returnType = "return_type_here"
        self.genericInstance = instanceObjList()

    def new(self, newName):
        hdl_code = "function %s is new %s\r\n" % (newName, self.name)
        hdl_code = hdl_code + indent(1)+"generic (\r\n"
        # todo: generic types here.
        if not self.genericInstance:
            for item in genericList:
                self.genericInstance.add(item,"<new value>")
        hdl_code = hdl_code + self.genericInstance.code()
        hdl_code = hdl_code + indent(1)+");\r\n"

    def declaration(self):
        hdl_code = self._code()
        hdl_code = hdl_code + indent(0) + ("return %s;\r\n" % self.returnType)
        return hdl_code

    def _code(self):
        hdl_code = indent(0) + ("function %s" % self.name)
        if (self.generic):
            hdl_code = hdl_code + ("\r\n")
            hdl_code = hdl_code + indent(1) + ("generic (\r\n")
            # todo: generic types here.
            hdl_code = hdl_code + self.generic.code()
            hdl_code = hdl_code + indent(1) + (")\r\n")
            hdl_code = hdl_code + indent(1) + ("parameter")
        if (self.parameter):
            hdl_code = hdl_code + indent(1) + (" (\r\n")
            hdl_code = hdl_code + self.parameter.code()
            hdl_code = hdl_code + indent(1) + (")\r\n")
        return hdl_code

    def code(self):
        hdl_code = self._code()
        hdl_code = hdl_code + indent(0) + ("return %s is\r\n")
        hdl_code = hdl_code + self.variable.code()
        hdl_code = hdl_code + indent(0) + ("begin\r\n")
        hdl_code = hdl_code + self.functionBody.code()
        hdl_code = hdl_code + indent(0) + ("end %s;\r\n" % self.name)
        return hdl_code

class componentObj:
    def __init__(self, name):
        self.name    = name
        self.generic = genericList()
        self.port    = portList()
        self.filename = ""
    def code(self):
        hdl_code = indent(0) + ("component %s is\r\n" % self.name)
        if (self.generic):
            hdl_code = hdl_code + indent(1) + ("generic (\r\n")
            hdl_code = hdl_code + self.generic.code()
            hdl_code = hdl_code + indent(1) + (");\r\n")
        else:
            hdl_code = hdl_code + indent(1) + ("--generic (\r\n")
            hdl_code = hdl_code + indent(2) + ("--generic_declaration_tag\r\n")
            hdl_code = hdl_code + indent(1) + ("--);\r\n")
        if (self.port):
            hdl_code = hdl_code + indent(1) + ("port (\r\n")
            hdl_code = hdl_code + self.port.code()
            hdl_code = hdl_code + indent(1) + (");\r\n")
        else:
            hdl_code = hdl_code + indent(1) + ("--port (\r\n")
            hdl_code = hdl_code + indent(2) + ("--port_declaration_tag\r\n")
            hdl_code = hdl_code + indent(1) + ("--);\r\n")
        hdl_code = hdl_code + indent(0) + ("end component;\r\n")
        hdl_code = hdl_code + "\r\n"
        return hdl_code

class componentList(dict):
    def add(self,name):
        self[name] = componentObj(name)
    def code(self):
        hdl_code = ""
        for j in self.list:
            hdl_code = hdl_code + self.list[j].code()
        return hdl_code

class instanceObj:
    def __init__(self, name, value):
        self.name = name
        self.value = ""
    def code(self):
        hdl_code = indent(2) + ("%s => %s,\r\n" % (self.name, self.value))
        return hdl_code

class instanceObjList(dict):
    def add(self, name, value):
        self[name] = instanceObj(name,value)
    def code(self):
        return VHDLenum(self)

class componentInstanceObj:
    def __init__(self, instance_name, component_name):
        self.instance_name  = instance_name
        self.component_name = component_name
        self.generic = instanceObjList()
        self.port    = instanceObjList()
        self.filename = ""
    def code(self):
        hdl_code = indent(0) + ("%s : %s\r\n" % (self.instance_name, self.component_name))
        if (self.generic):
            hdl_code = hdl_code + indent(1) + ("generic map(\r\n")
            hdl_code = hdl_code + self.generic.code()
            hdl_code = hdl_code + indent(1) + (")\r\n")
        if (self.port):
            hdl_code = hdl_code + indent(1) + ("port map(\r\n")
            hdl_code = hdl_code + self.port.code()
            hdl_code = hdl_code + indent(1) + (");\r\n")
        hdl_code = hdl_code + "\r\n"
        return hdl_code

class componentInstanceList(dict):
    def add(self,name):
        self[name] = componentInstanceObj(name)
    def code(self):
        hdl_code = ""
        for j in self.list:
            hdl_code = hdl_code + self.list[j].code()
        return hdl_code

class entityObj:
    def __init__(self, name):
        self.name = name
        self.generic = genericList()
        self.port = portList()

    def code(self):
        hdl_code = indent(0) + ("entity %s is\r\n" % self.name)
        if (self.generic):
            hdl_code = hdl_code + indent(1) + ("generic (\r\n")
            hdl_code = hdl_code + self.generic.code()
            hdl_code = hdl_code + indent(1) + (");\r\n")
        else:
            hdl_code = hdl_code + indent(1) + ("--generic (\r\n")
            hdl_code = hdl_code + indent(2) + ("--generic_declaration_tag\r\n")
            hdl_code = hdl_code + indent(1) + ("--);\r\n")
        if (self.port):
            hdl_code = hdl_code + indent(1) + ("port (\r\n")
            hdl_code = hdl_code + self.port.code()
            hdl_code = hdl_code + indent(1) + (");\r\n")
        else:
            hdl_code = hdl_code + indent(1) + ("--port (\r\n")
            hdl_code = hdl_code + indent(2) + ("--port_declaration_tag\r\n")
            hdl_code = hdl_code + indent(1) + ("--);\r\n")
        hdl_code = hdl_code + indent(0) + ("end %s;\r\n" % self.name)
        hdl_code = hdl_code + "\r\n"
        return hdl_code

class architectureObj:
    def __init__(self, name, entity_name):
        self.name = name
        self.entityName = entity_name
        self.signal = signalList()
        self.constant = constantList()
        self.component = componentList()
        self.functions = ""
        self.procedures = ""
        self.customTypes = genericCodeBlock(1)
        self.declarationHeader = genericCodeBlock(1)
        self.declarationFooter = genericCodeBlock(1)
        self.bodyCodeHeader = genericCodeBlock(1)
        self.instances = ""
        self.blocks = ""
        self.process = ""
        self.bodyCodeFooter = genericCodeBlock(1)

    def code(self):
        hdl_code = ""
        hdl_code = indent(0) + ("architecture %s of %s is\r\n" % (self.name, self.entityName))
        hdl_code = hdl_code + "\r\n"
        if (self.declarationHeader):
            hdl_code = hdl_code + self.declarationHeader.code()
            hdl_code = hdl_code + "\r\n"
        if (self.constant):
            hdl_code = hdl_code + self.constant.code()
            hdl_code = hdl_code + "\r\n"
        if (self.customTypes):
            hdl_code = hdl_code + self.customTypes.code()
            hdl_code = hdl_code + "\r\n"
        if (self.component):
            hdl_code = hdl_code + self.component.code()
            hdl_code = hdl_code + "\r\n"
        if (self.signal):
            hdl_code = hdl_code + self.signal.code()
            hdl_code = hdl_code + "\r\n"
        hdl_code = hdl_code + indent(1) + ("--architecture_declaration_tag\r\n")
        hdl_code = hdl_code + "\r\n"
        hdl_code = hdl_code + indent(0) + ("begin\r\n")
        hdl_code = hdl_code + "\r\n"
        if (self.bodyCodeHeader):
            hdl_code = hdl_code + self.bodyCodeHeader.code()
            hdl_code = hdl_code + "\r\n"
        hdl_code = hdl_code + indent(1) + ("--architecture_body_tag.\r\n")
        hdl_code = hdl_code + "\r\n"
        if (self.bodyCodeHeader):
            hdl_code = hdl_code + self.bodyCodeFooter.code()
            hdl_code = hdl_code + "\r\n"
        hdl_code = hdl_code + indent(0) + ("end %s;\r\n" % self.name)
        hdl_code = hdl_code + "\r\n"
        return hdl_code

class basicVHDL:
    def __init__(self, entity_name, architecture_name):
        self.library      = libraryList()
        self.entity       = entityObj(entity_name)
        self.architecture = architectureObj(architecture_name, entity_name)

    def instance(self, instance_name, generic_list, port_list):
        self.tmpinst = componentInstanceObj()
        for j in self.entity.generic.list:
            self.tmpinst.generic.add(j.name,j.value)
        for j in generic_list:
            self.tmpinst.generic[j.name].value = [j.name]
        for j in self.entity.port.list:
            self.tmpinst.port.add(j.name,j.value)
        for j in port_list:
            self.tmpinst.generic[j.name].value = [j.name]
        return self.tmpinst.code()

    def write_file(self):
        hdl_code = self.code()

        if (not os.path.exists("output")):
            os.makedirs("output")

        output_file_name = "output/"+self.entity.name+".vhd"
        #to do: check if file exists. If so, emit a warning and
        #check if must clear it.
        output_file = open(output_file_name,"w+")
        for line in hdl_code:
            output_file.write(line)

        output_file.close()
        return True;

    def code(self):
        hdl_code = ""
        hdl_code = hdl_code + self.library.code()
        hdl_code = hdl_code + self.entity.code()
        hdl_code = hdl_code + self.architecture.code()
        return hdl_code
