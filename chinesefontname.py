#!/usr/bin/env python
import os
import sys
import commands
import xml.etree.cElementTree as ElementTree

ttf_file = os.path.basename(sys.argv[1])
name_xml = ttf_file + '.xml'
# Dump name table of the TTF file
(status, output) = commands.getstatusoutput("ttx -o %s -t name %s" % (name_xml, ttf_file))
if status != 0:
	print output
	exit(-1)

ET = ElementTree.parse(name_xml)
name = ET.getroot().find("name")
record_template = "namerecord[@platformID='%s'][@langID='%s'][@nameID='%s']"
chinese_record = name.find(record_template % ('3', '0x804', '1'))
english_record = name.find(record_template % ('1', '0x0', '1'))
english_record.text = chinese_record.text
english_record.set('platEncID', '25');
english_record.set('langID', '0x21');

ET.write("test.xml", encoding="utf-8", xml_declaration=True)

(status, output) = commands.getstatusoutput("ttx -o %s -m %s -t name %s" % ('new_'+ttf_file, ttf_file, 'test.xml'))
if status != 0:
	print output
else:
	print 'Success!'

