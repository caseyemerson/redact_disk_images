import pyewf

ewf_handle = pyewf.handle()

ewf_handle.open(["terry.E01"])	# open E01 image

ewf_handle.seek_offset(12816474, 0)	# go to the feature offset

feature = ewf_handle.read(35)	# start at the offset and read 35 bytes

print(feature)	# print the feature info@xceedsoft.com



ewf_handle.write_buffer("\x00",1)	# THIS LINE FAILS
# THE PROBLEM APPEARS TO BE IN 
# ~/Tools/libewf-20130416/pyewf/pyewf_handle.c 
# around line 1116



ewf_handle.close()	# close the file



# ewf_handle.write_random("\x00\x00\x00", 3, 12816474)

# offset 12816474, 35 bytes i.n.f.o.@.x.c.e.e.d.s.o.f.t...c.o.m
