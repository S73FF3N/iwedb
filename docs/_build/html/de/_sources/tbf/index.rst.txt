TBF
===

The TBF-Menu contains the menu points "Contracts" and "Reports".

Contracts
---------

In this menu all contracts are listed, which contains the contract part "Technical Operation". This menu offers all funtions analog to "Contract List".

Reports
-------

The menu point "Reports" is used to koordinate reports and other extern services.

**Type**: Type of the report: WKP / ZOP / gearpox endoscopy / Safety check / ZÜS BFA / general overhaul winch / GÜ / Change board crane / lattice mast check / DGUV V3
**WEA**: WAE, which are involved to the report; For excample: SEN300488, SEN300489, SEN300490, SEN300491, SEN300492, SEN300493
**All**: Number of time units, which control the repetition frequenzy of report dates; Format: positive natural numbers
**Intervall**: Time units, which control the repetition frequency of report dates; Days / months / Years
**For**: Number of time units, which control the duraation of report dates; Format: positive natural numbers
**Duration**: Time units, which control the duration of report dates; Days / Months / Years
**Target date first provision**: Planned date first provision / first date of the report
**Responsible**: Responsible employee from DWT

Reports fundamental consisting of one or more dates per linked turbine. In the list view of a report under the filters all dates per state (Overdue / Commisioned / Registred / Done / Report recieved /
account recieved) are listed, bevore at the end of the site a table for the report exist.

The filters "Type","Windfarm" and "Responsible" just affect to the superordinate report and just indirect to the dates.

Report Detail
^^^^^^^^^^^^^
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