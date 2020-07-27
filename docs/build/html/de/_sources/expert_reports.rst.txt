Expert Reports
==============

The menu "Reports" consists of the tabs "TO" and "Customer management". Here all dates and reports are listed, which are relevant for the selected department.

The structure of the two menu points is identical, and will be clarified generally in the following sections "Report List", "Report Detail" and "Report Form".

Report List
-----------

The report list is devided into dates and reports.

The selection of the displayed reports and dates can be limited with the following filters:

    *   Type
    *   Wind Farm (multiple selection possible)
    *   Responsible (multiple selection possible)
    *   Date (between ... and ...)

Dates are shown in the first few tables. They are sorted in their actual states (Remaining Dates / Ordered Dates / Confirmed Dates / Scheduled Dates / Executed Dates/ Report Recieved).
The coloration visualised the actual need for action:

    *   red: acute need for action
    *   yellow: need for action
    *   green: no need for action

At the top of the tables a counter shows, how much dates need action (red or yellow). Also under every head line the time range is shown, in which the dates are located. In the last two
columns of the tables its possible to delete or edit a date.

At the end of the site a table with all reports exist. Reports fundamental consisting of one or more dates per linked turbine. Above the report table a counter exist, which shows how much
reports are not terminated yet (coloured red).

With the buttons at the upper right corner of the report list its possible to create a new report or date, or to import the actual selection into Excecl-Format.

Report Detail
-------------

Over the table "Report" it´s possible to select individual reports. In this detail view the information and dates from the report are listed.

The single "Edit" button at the top of the detail view can be used to chnage the properties of a report. With the "+" button at the top of the detail view its possible to add dates to a report.
It's possible to edit more dates at once with the two "Edit" buttons over the table at the bottom. After pressing the button a formula appears, where all dates have to be selected wich should be
changed. After selecting the dates, the properties of this dates can be changed at once.

The third button at the top of the detail view creates a order, which can be changed individual. A new site appears, where some dates are listed. Now its necessary to select a date and press the arrow
button at the right side beside the table. After this a order form will be generated.

Per report a commentary function is available, which should be used superordinate. Also for each date it´s possible to create comments individually.

Report Form
-----------

The report formula is available over the "+" button at the upper right side of the report list.

A report gets characterized by the following properties:

**Type**: Type of the report: WKP / ZOP / gearpox endoscopy / Safety check / ZÜS BFA / general overhaul winch / GÜ / Change board crane / lattice mast check / DGUV V3
WEA: WAE, which are involved to the report; For excample: SEN300488, SEN300489, SEN300490, SEN300491, SEN300492, SEN300493
Wind Farm: Wind farm the WEA is located; For excample: Baalberge
Part of Contract: Yes / NO / Stateful / Capital
**Every**: Number of time units, which control the repetition frequenzy of report dates; Format: positive natural numbers
**Time interval**: Time units, which control the repetition frequency of report dates; Days / months / Years
**For**: Number of time units, which control the duraation of report dates; Format: positive natural numbers
**Duration**: Time units, which control the duration of report dates; Days / Months / Years
**Scheduled first execution**: Planned date first provision / first date of the report
**Responsible**: Responsible employee from DWT

Date Form
---------

Dates can get changed and added. Adding a new date is possible over the report detail view, while editing a date is possible over the Report list over the "Edit" buttons in the tables.

A date contains the following properties:

    *   Turbine
    *   Order Date
    *   Execution Date
    *   Scheduled Date
    *   Service Provider
    *   **Status**
    *   Comment

If the state of a date is at least "executed", the next dates can be calculated over a checkbox, based on the last execution date.
