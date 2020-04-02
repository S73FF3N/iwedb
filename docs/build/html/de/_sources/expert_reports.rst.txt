Expert Reports
==============

The menu "Reports" consists of the tabs "TBF" and "Customer management". Here all dates and reports are listed, which are relevant for the selected department.

The structure of the two menu points is identical, and will be clarified generally in the following sections "Report List" and "Report Detail".

A report gets characterized by the following properties:


**Type**: Type of the report: WKP / ZOP / gearpox endoscopy / Safety check / ZÜS BFA / general overhaul winch / GÜ / Change board crane / lattice mast check / DGUV V3
WEA: WAE, which are involved to the report; For excample: SEN300488, SEN300489, SEN300490, SEN300491, SEN300492, SEN300493
Wind Farm: Wind farm the WEA is located; For excample: Baalberge
Contract Part: Yes / NO / Stateful / Capital
**All**: Number of time units, which control the repetition frequenzy of report dates; Format: positive natural numbers
**Intervall**: Time units, which control the repetition frequency of report dates; Days / months / Years
**For**: Number of time units, which control the duraation of report dates; Format: positive natural numbers
**Duration**: Time units, which control the duration of report dates; Days / Months / Years
**Target date first provision**: Planned date first provision / first date of the report
**Responsible**: Responsible employee from DWT

Report List
-----------

Reports fundamental consisting of one or more dates per linked turbine. In the list view of a report under the filters all dates per state (Remaining Dates / Ordered Dates
/ Confirmed Dates / Scheduled Dates / Executed Dates / Report recieved) are listed, bevore at the end of the site a table for the report exist.

The selection of the displayed reports and dates can be limited with the following filters:

    *   Type
    *   Wind Farm (multiple selection possible)
    *   Responsible (multiple selection possible)

Report Detail
-------------

Over the table "Report" it´s possible to value individual reports. In this detail view the information and dates from the report are listed.

Its important to observe, that with the crating of a report not the dates are generated automatically. Herefore the button "Create Date" exist. After unsing the button the dates,based on the planning
date of the fist provision, the time frequency and provision, are generated and displayed tabular. Also now individual dates can be added with the button "+Termin".

A date contains the following properties:

    *   **Planning Date**: original date of provision
    *   **Report**: Obtain to the primary report object
    *   **WEA**: A date always contains an obtain to an individual WEA
    *   **State**: Overdue / Commisioned / Registred / Done / Report recieved / Account recieved
    *   Provider: Obtain to the commisioned company (Actor)
    *   Contract Part: Yes / No / Stateful / capital
    *   Check date: Real provision date
    *   Commentary: Possibility, to give extra information

If more dates have to be changed, the formula "more dates" helps out. Here it´s possible to select, which dates have to be changed in which way.

Per report a commentary function is available, which should be used superordinate. Also for each date it´s possible to create comments individually.
