import datetime
import time
import os
import subprocess
import sys
import yaml
import glob
import shutil
import git
import boto3
from botocore.config import Config
def compile_sketch(spec):
    sketch = None
    board = None
    for file in glob.glob("*.ino"):
            #print(file)
            print("------------------------------------------------------")
    my_file = file
    fileA = open(my_file, 'rb')
    fileB = open("sketch.ino", 'wb')
    shutil.copyfileobj(fileA, fileB)
    #os.rename(my_file, 'sketch.ino')
        

    if "sketch" not in spec:
        print("Sketch file not specified, unable to compile")
        
        
        sys.exit(1)
    else:
        sketch = spec["sketch"]

    if "target" not in spec:
        print("Compilation target not specified, unable to compile")
        sys.exit(1)
    else:
        if "board" not in spec["target"]:
            print("Target board type not specified, unable to compile")
            sys.exit(1)
        else:
            board = spec["target"]["board"]
            print(f"Compiling {sketch} for board type {board}")
        if "url" in spec["target"]:
            _add_arduino_core_package_index(spec["target"]["url"])
        if "core" in spec["target"]:
            (core_name, core_version) = _parse_version(spec["target"]["core"])
            core_name_version = f"{core_name} v{core_version}" \
                if core_version is not None else f"{core_name} (latest)"
            print(f"Installing core {core_name_version}... ", end="")
            success = _install_arduino_core(core_name, core_version)
            print("Done!" if success else "Failed!")
            if not success:
                sys.exit(1)

    if "libraries" in spec:
        for lib in spec["libraries"]:
            (lib_name, lib_version) = _parse_version(lib)
            lib_name_version = f"{lib_name} v{lib_version}" \
                if lib_version is not None else f"{lib_name} (latest)"
            print(f"Installing library {lib_name_version}... ", end="")
            success = _install_arduino_lib(lib_name, lib_version)
            print("Done!" if success else "Failed!")
            if not success:
                sys.exit(1)

    output_path = sketch.split(".")[0]
    
    
    
    if "version" in spec:
        output_path += "_v" + spec["version"].replace(".", "_")
    build_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path += "_" + build_date + "Z"
    output_path += ".bin"
    print(f"Sketch will be compiled to current Directory")

    success = _compile_arduino_sketch(sketch, board, output_path)
    print("Compilation completed!" if success else "Compilation failed!")
    

def _parse_version(line):
    if "==" in line:
        (name, version) = line.split("==", 1)
    else:
        (name, version) = (line.strip(), None)
    return (name, version)


def _add_arduino_core_package_index(url):
    return _run_shell_command(["arduino-cli", "core", "update-index",
                               "--additional-urls", url])


def _install_arduino_core(name, version=None):
    core = f"{name}@{version}" if version is not None else name
    return _run_shell_command(["arduino-cli", "core", "install", core])


def _install_arduino_lib(name, version=None):
    lib = f"{name}@{version}" if version is not None else name
    return _run_shell_command(["arduino-cli", "lib", "install", lib])


def _compile_arduino_sketch(sketch_path, board, output_path):
    os.makedirs("dist/", exist_ok=True)
    print(sketch_path)
    print("+++++++++++++++++++")
    sketch=os.getcwd()
    print(sketch)

    flag_list = ''
    for item, value in os.environ.items():
        if item.startswith("AF_"):
            flag_list += """-D{}="{}" """.format(item,value)

    compile_flags=r"""compiler.cpp.extra_flags='{}'""".format(flag_list)
    return _run_shell_command(["arduino-cli", "compile","-b", board,"--output-dir" , sketch,"--build-property", compile_flags, sketch_path],stdout=True)

    sketch_path+=".bin"
    
    
    
    
def genUrl (bucket,s3_file):
    s3 = boto3.client('s3',aws_access_key_id=access,
                      aws_secret_access_key=secret,region_name = 'ap-south-1',config=Config(signature_version="s3v4"),)
    
    try:
        x = s3.generate_presigned_url('get_object', Params={'Bucket':bucket,'Key': s3_file,}, ExpiresIn = 3600,)
        print (x)
        return x
    except ClientError as e:
        logging.error(e)
        return None
    
    
    
def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=access,
                      aws_secret_access_key=secret,region_name = 'ap-south-1')

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        
        #print (x)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def _run_shell_command(arguments, stdout=False, stderr=True):
    print(arguments)
    process = subprocess.run(arguments, check=False, capture_output=True)
    if stdout and len(process.stdout) > 0:
        print("> %s" % process.stdout.decode("utf-8"))
    if stderr and len(process.stderr) > 0:
        print("ERROR > %s" % process.stderr.decode("utf-8"))
    return (process.returncode == 0)


if __name__ == "__main__":
   
    objecturl=str(os.environ['GITHUB_REPOURL'])
    access = str(os.environ['AWS_ACCESS_KEY'])
    secret = str(os.environ['AWS_SECRET_KEY'])
    print(objecturl)
    #print(os.listdir())
    #print(os.getcwd())
    objectdir='sketch'
    git.Repo.clone_from(objecturl, '/usr/src/sketch')
    print("Repository elements are.....")
    os.chdir('/usr/src/sketch')
    
    #print("***************LookAbove**************")
    try:
        print(os.listdir())
        f = open("project.yaml", "r")
        spec = yaml.safe_load(f)
        compile_sketch(spec)
        #print(os.getcwd())
        print("UPLOADING>>>>>>>>>>>>>>")
        #Specify your bucket name below
        uploaded = upload_to_aws('sketch.ino.bin', 'arduino-binaries-tattva-cloud', 'sketch.bin')
        time.sleep(5)
        link=genUrl('arduino-binaries-tattva-cloud',"sketch.bin")
        print("*****************************above link can be used to sownload the binary************************************")    
            
        sys.exit(0)
    except IOError as e:
        print(e)
        print(os.getcwd())
        print(os.listdir())
        os.chdir('/usr/src/sketch/')
        print(os.listdir())
        os.remove("sketch.ino") 
        sys.exit(1)
    except yaml.YAMLError as e:
        print("Something wrong with the syntax of project.yaml: %s" % e)
        print(os.getcwd())
        os.remove("sketch.ino") 
        sys.exit(1)
