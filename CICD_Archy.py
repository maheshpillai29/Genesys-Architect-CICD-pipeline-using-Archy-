import json
import subprocess
import os
import re


optionsFilePath="C:\\Archy\\OptionsFiles\\DEVOptions.yaml"
filesDirectory="C:\\Archy\\CCI-222"

#sourceFlowName = input("Enter the source flow name: ")
sourceFlowName="SIT_Retail & Retail Support OpenHours"
print("You entered:", sourceFlowName)
#sourceDivision = input("Enter the source Division: ")
sourceDivision="SIT Retail"
print("You entered:", sourceDivision)

#targetFlowName = input("Enter the target flow name: ")
targetFlowName="MP_UAT_Retail_Export_Test"
print("You entered:", targetFlowName)
#targetDivision = input("Enter the target division name: ")
targetDivision="UAT Retail"
print("You entered:", targetDivision)


def executeArchyCommand(command):
    stdout=""
    stderr=""
    returnCode=10
    try:
        os.chdir("C:\\Archy")
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        returnCode=result.returncode
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    return stdout,stderr,returnCode

def createFlow():
    try:
        os.chdir("C:\\Archy")
        command = "archy create --file MP_NCS_MainClosed_Test.yaml --optionsFile PRODOptions.yaml"
        # Run the command, capture output as byte string
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Decode stdout and stderr to string
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        
        if result.returncode==0:
            print("Flow created successfully")
        # Print stdout (if any)
        if stdout:
            print(f"STDOUT:\n{stdout}")
        
        # Print stderr (if any)
        if stderr:
            print(f"STDERR:\n{stderr}")
        
        # Print return code
        print(f"Return Code: {result.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        # Optionally, handle specific error cases based on e.returncode or e.output

    # Check if the command was successful
    if result.returncode == 0:
        print("Command executed successfully.")
        #print(result.stdout)
    else:
        print("Error executing command.")
        # Print the error message, if any
        print("Error:")
        print(result.stderr)

    #def copyFlow(sourceEnvironment,targetEnvironment):

def replaceTextInYamlFile(inputYamlFilePath,inputSubstitutionJsonFilePath,sourceFlowName,targetFlowName,sourceEnvironment,targetEnvironment):
    with open(inputYamlFilePath, 'r') as file:
        yamlSource = file.read()

    jsonFile = open(inputSubstitutionJsonFilePath)
    data = json.load(jsonFile)
    for substitutionsArray in data['substitutions']:
        find=substitutionsArray[sourceEnvironment]
        replace=substitutionsArray[targetEnvironment]
        yamlSource = yamlSource.replace(find, replace)
    yamlSource=yamlSource.replace("name: "+sourceFlowName,"name: "+targetFlowName) #replace flow name
    yamlSource=yamlSource.replace("division: "+sourceEnvironment,"division: "+targetEnvironment) #replace divison name 
    jsonFile.close()
        
    # Write the file out again
    with open(filesDirectory+"\\"+targetFlowName+".yaml", 'w') as file:
        file.write(yamlSource)
        file.flush()
        file.close()
    return targetFlowName+".yaml"

def downloadSourceYAMLFile():
    command = "archy export --flowName \""+sourceFlowName+"\" --flowType \"inboundcall\" --exportType \"yaml\" --outputDir \""+filesDirectory+"\" --optionsFile \""+optionsFilePath+"\""
    print("Exporting source file..")
    stdout, stderr,returnCode=executeArchyCommand(command)
    #print(f"Result:\n{stdout}\n{stderr}")
        
    outputFileName=""
    if returnCode==0:
        match = re.search(r"Export file name: '([^']+)'", stdout)
        if match:
            outputFileName=match.group(1)
            if outputFileName!="":
                print(f"Output Filename - {outputFileName}")
                #print(match.group(1))  # Return the matched filename
                print(f"Flow exported successfully")
                print(f"Creating target YAML file..")
                convertedFileName=replaceTextInYamlFile(filesDirectory+"\\"+outputFileName,"C:\\Terraform\\ARchyTesting\\data.json",sourceFlowName,targetFlowName,sourceDivision,targetDivision)
                print(f"Target file created")
                print(f"Copying the file to the target environment..")
                checkInTargetFlow(convertedFileName)
            else:
                print("No Exported File")  # Return None if the pattern is not found
        else:
            print("No value")  # Return None if the pattern is not found
        
    else:
        print(f"Error: {stderr}")

def checkInTargetFlow(fileName):
    command="archy update --file \""+filesDirectory+"\\"+fileName+"\" --optionsFile \""+optionsFilePath+"\""
    stdout, stderr,returnCode=executeArchyCommand(command)
    #print(f"Result:\n{stdout}\n{stderr}")
    if returnCode==0:
        print(f"Flow copied successfully to target")
    else:
        print(f"Error: {stderr}")

downloadSourceYAMLFile()