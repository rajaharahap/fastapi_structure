import sys
import shutil
import os

path = os.path.abspath(os.getcwd())
# print(sys.argv[0].lower())
if sys.argv[1].lower()=='-m':
    if len(sys.argv)>2:
        if os.path.exists(path+'/modules/' +sys.argv[2]):
            print(f"Module '{sys.argv[2]}' is exist")
        else:
            os.makedirs(path+'/modules/' +sys.argv[2])
            f = open(path+'/modules/' +sys.argv[2]+'/__init__.py', 'w')
            f.write('__all__=[]')
            f.close()

            f = open(path+'/modules/__init__.py','r')
            c = f.read() + f'\nfrom modules.{sys.argv[2]} import *'
            f.close()

            f = open(path+'/modules/__init__.py','w')
            f.write(c)
            f.close()
    else:
        print("param not complete")

elif sys.argv[1].lower()=='-c':
    if len(sys.argv)>3:
        if os.path.exists(path+'/modules/' +sys.argv[3]+'/'+ sys.argv[2]+'.py'):
            print(f"Class '{sys.argv[2]}' is exist...")
        else:
            print(path+'/base/class__.py')
            print(path+'/modules/' +sys.argv[3]+'/'+ sys.argv[2]+'.py')
            shutil.copyfile(path+'/base/class__.py', path+'/modules/' +sys.argv[3]+'/'+ sys.argv[2]+'.py')
            # print(path+'/modules/' + sys.argv[3]+'/' +sys.argv[2]+'.py')
            f = open(path+'/modules/' + sys.argv[3]+'/' +sys.argv[2]+'.py', 'r')
            old_name = sys.argv[2]
            class_name = old_name[:1]+old_name[1:len(old_name)]
            module_name = sys.argv[3]
            print(class_name)
            textwrap = f.read()
            #print(textwrap)
            textwrap = str(textwrap).replace("class__", f"{class_name}")
            textwrap = str(textwrap).replace("module__", f"{module_name}")
            f.close()


            f = open(path+'/modules/' + sys.argv[3]+'/' +sys.argv[2]+'.py', 'w')
            f.write(textwrap)
            f.close()

            f = open(path+'/modules/'+ sys.argv[3] +'/__init__.py', 'r')
            textwrap = f.read()
            textwrap = textwrap.replace("]",f""""{sys.argv[2]}",
            ]
            """)
            f.close()

            f = open(path+'/modules/'+ sys.argv[3] +'/__init__.py', 'w')
            f.write(textwrap)
            f.close()
    else:
        print("param not complete")

