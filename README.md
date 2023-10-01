
# Mitre Att&ck - evaluation [Graphic mode]

    py .\mitre2graph.py <year>

# Result
![example of a chart obtained with the script](https://github.com/ZA512/mitre_evaluation/blob/main/img/screenshot1.png)

# Mitre Att&ck - evaluation [All result in a html table]

    py .\mitre2html.py <year>

# Result
just open the html file created.
In the "Mitre Evaluation html" folder, you'll find the tables 2021, 2022 and 2023. You can use them without running the script. But it may be a good idea to delete the solutions you don't want and manage the table only with the chosen solutions.

![example of a chart obtained with the script](https://github.com/ZA512/mitre_evaluation/blob/main/img/screenshot2.png)

# Don't work before 2021
Since 2021 they have frozen the json format.


# Explanation : Detection Categories
### **N/A :** 
Vendor did not have visibility on the system under test. The vendor must state before the evaluation what systems they did not deploy a sensor on to enable Not Applicable to be in scope for relevant steps.

###### Examples : 
*No sensor was deployed in the Linux systems within the environment to capture command-line activity, which would have been required to satisfy the detection criteria of the technique under test.*

### **NONE :** 
No data was made available within the capability related to the behavior under test that satisfies the assigned detection criteria. There are no modifiers, notes, or screenshots included with a None.

**TELEMETRY :** Minimally processed data collected by the capability showing that event(s) occurred specific to the behavior under test that satisfies the assigned detection criteria. Evidence must show definitively that behavior occurred and be related to the execution mechanism (did happen vs may have happened). This data must be visible natively within the tool and can include data retrieved from the endpoint.

###### Examples : 
*Command-line output is produced that shows a certain command was run on a workstation by a given username. There is a remote shell component within the capability that can be used to pull native OS logs from a system suspected of being compromised for further analysis.*

### **GENERAL :** 
Processed data specifying that malicious/abnormal event(s) occurred, with relation to the behavior under test. No or limited details are provided as to why the action was performed (tactic), or details for how the action was performed (technique).

##### Examples : 
*A detection describing "cmd.exe /c copy cmd.exe sethc.exe" as abnormal/malicious activity, but not stating it's related to Accessibility Features or a more specific description of what occurred.
A “Suspicious File” detection triggered upon initial execution of the executable file.
A detection stating that "suspicious activity occurred" related to an action but did not provide detail regarding the technique under test.*

### **TACTIC :** 
Processed data specifying ATT&CK Tactic or equivalent level of enrichment to the data collected by the capability. Gives the analyst information on the potential intent of the activity or helps answer the question "why this would be done". To qualify as a detection, there must be more than a label on the event identifying the ATT&CK Tactic, and it must clearly connect a tactic-level description with the technique under-test.

##### Examples :
*A detection called “Malicious Discovery” is triggered on a series of discovery techniques. The detection does not identify the specific type of discovery performed.
A detection describing that persistence occurred but not specifying how persistence was achieved.*

### **TECHNIQUE :** 
Processed data specifying ATT&CK Technique, Sub-Technique or equivalent level of enrichment to the data collected by the capability. Gives the analyst information on how the action was performed or helps answer the question "what was done" (i.e. Accessibility Features or Credential Dumping). To qualify as a detection, there must be more than a label on the event identifying the ATT&CK Technique ID (TID), and it must clearly connect a technique-level description with the technique under-test.

##### Examples :
*A detection called "Credential Dumping" is triggered with enough detail to show what process originated the behavior against lsass.exe and/or provides detail on what type of credential dumping occurred.
A detection for "Lateral Movement with Service Execution" is triggered describing what service launched and what system was targeted.*

# Explanation : Modifier Detection Types
The configuration of the capability was changed since the start of the evaluation. This may be done to show additional data can be collected and/or processed. The Configuration Change modifier may be applied with additional modifiers describing the nature of the change, to include:

-   **Data Sources**  - Changes made to collect new information by the sensor. In graphics is represented by **"DS"**.
-   **Detection Logic**  - Changes made to data processing logic. In graphics is represented by **"DL"**.
-   **UX**  - Changes related to the display of data that was already collected but not visible to the user. In graphics is represented by **"UX"**.

###### Examples : 
*The sensor is reconfigured to enable the capability to monitor file activity related to data collection. This would be labeled with a modifier for Configuration Change-Data Sources.
A new rule is created, a pre-existing rule enabled, or sensitivities (e.g., blacklists) changed to successfully trigger during a retest. These would be labeled with a modifier Configuration Change-Detection Logic.
Data showing account creation is collected on the backend but not displayed to the end user by default. The vendor changes a backend setting to allow Telemetry on account creation to be displayed in the user interface, so a detection of Telemetry and Configuration Change-UX would be given for the Create Account technique.*
