# Genesys Flow Management Automation with Python

This Python script automates the management and transformation of Genesys Cloud flows using the Archy CLI. It streamlines the export, modification, and deployment of flow configurations in YAML format, simplifying multi-environment deployments.

---

## **Key Features**

- **Export Genesys Flow**: Automates exporting flows as YAML files using `archy export`.
- **Dynamic YAML Modification**: Replaces environment-specific attributes like flow names and divisions using a JSON substitution file.
- **Flow Creation and Update**: Generates and uploads modified flows to the target environment using `archy update`.
- **Error Handling**: Comprehensive logging and meaningful error messages for debugging.

---

## **Requirements**

### **Software**
- **Python 3.x**: The script is compatible with Python 3.x.
- **Archy CLI**: Ensure Archy is installed and configured on your system.
- **Genesys Cloud**: Proper configurations and permissions are required for using Archy with Genesys Cloud.

### **Python Libraries**
- `json`: For reading substitution data.
- `subprocess`: For executing Archy commands.
- `os`: For file and directory handling.
- `re`: For regular expression parsing.

---

## **Configuration**

### **Input Files**
1. **YAML Options File**:
   - **Path**: `C:\\Archy\\OptionsFiles\\DEVOptions.yaml`
   - Contains configuration options for the Archy commands.

2. **JSON Substitution File**:
   - **Path**: `C:\\Terraform\\ARchyTesting\\data.json`
   - Specifies key-value pairs for replacing environment-specific attributes.

### **Directories**
- **Source Directory**: `C:\\Archy\\CCI-222`
  - The directory where the exported YAML file will be saved.
- **Target Directory**: Same as the source directory, but new files are created with target environment details.

### **Script Variables**
- **Source Flow**: `sourceFlowName` (e.g., "SIT_Retail & Retail Support OpenHours").
- **Source Division**: `sourceDivision` (e.g., "SIT Retail").
- **Target Flow**: `targetFlowName` (e.g., "MP_UAT_Retail_Export_Test").
- **Target Division**: `targetDivision` (e.g., "UAT Retail").

---

## **How It Works**

1. **Export Flow**:
   - The `downloadSourceYAMLFile()` function calls Archy to export the specified source flow as a YAML file.

2. **Modify YAML**:
   - The `replaceTextInYamlFile()` function reads the exported YAML and applies substitutions based on the JSON file and custom inputs.

3. **Create and Update Flow**:
   - The modified YAML is saved as a new file and uploaded to the target environment using the `archy update` command.

4. **Error Management**:
   - The script captures errors during command execution and provides detailed logs for debugging.

---

## **Example Usage**

1. Configure the input paths, flow names, and divisions in the script.
2. Run the script:
   ```bash
   python CICD_Archy.py
