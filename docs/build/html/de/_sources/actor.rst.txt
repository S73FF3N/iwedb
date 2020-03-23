Actor
=====

An actor is a company which is active in the wind industry. He has the following properties:

    *   **Name**: Name of the company; For excample: Deutsche Windtechnik X-Service GmbH
    *   Address: Postal address of the company; For excample: Heideweg 2-4
    *   Postal code: For excample: 49086
    *   City: For excample: Osnabrück
    *   **Country**: For excample Deutschland/Germany
    *   Phone: Phone Number; For excample: +49 541 38 05 38 100
    *   Mail: E-Mail address; For excample: info@deutsche-windtechnik.com
    *   Web: Homepage; For excample: http:\\deutsche-windtechnik.com
    *   Sector: sector of the company; Beispiel: Service, Technincal Operations
    *   Head Oranisation: holding company; For excample: Deutsche Windtechnik AG

Actor List
----------

The Actor List lists all usable companies from the database alphabetical. Over the button "Add Actor" new companies can be added. With "Custom Export" the actual list with the used filters get exported into
Excel. The following filters are available:

    *   Name: Name of the company
    *   Country
    *   City
    *   Sector: Sector of the company; multiple selection possible

Actor Detail
------------

Under the name of the company and the Edit-Button properties of the actors are displayed.

Its possible to assign employees with the "Add Employee" button. They have the following properties:

    *   **Name**: First and last name of the employee; For Excample: Max Mustermann
    *   Function: Function of the employee; For Excample: Head of Sales
    *   Phone: Phone Number; For Excample: +49 451 38 05 38 100
    *   Alternative Phone
    *   Mail: E-Mail address; For excample: info@deutsche-windtechnik.com
    *   Address: Postal address; For excample: Heideweig 2-4
    *   Postal Code: For excample: 49086
    *   City: For excample: Osnabrück

If a company got assigned to a holding company over the "Head Organisation", the row "Head Organisation occured, which lists all doughter companies of the head company. Also in the doughter company the
head company is linked.

As soon as a turbine owns in the properties "Developer", "Asset Manager", "Technical Operator", "Commercial Operator", "Service" or "Owner" the same object as the actor, a row appears in the detail view.
It says for how much WEA the actor "Developer" / "Asset Manager" / "Technical Operator" / "Service Provider" or "Owner" be. With one click on one row it folds out and shows all turbines, sorted by their
technologies.

The employees are listed to their company in the detail view. For individual employees there also exist a detail view with all their properties. Also the formula for changing the
employee properties can be opened over the "Shift"-Symbol. The formula is available over the detail view from the employee too ("Edit"). Over the button "Set inactive" employees also can get set inactive.
This should be used if an employee isn't a member of the company any more.

Below the employee Project/Pool projects and contents, in which the actor is involved, are listed. Here is a difference between "direkt" and "indirekt". There is a direct involvation, if the actor is
linked as a "Negotiation Partner" in his project. For contracts there is a direct involve, if the actor got listed in the contractual propertie "Contractuaal Partner". Indirect connections are caused by
turbines, which are connected to the project/contract. If one of the turbines are connected to the actor over the proerties "Asset Manager", "Commercial Operator", "Technical Operator" or "Owner", the
project or contract appears under "indirect".

With the button "add file" files can be uploaded, which are visible in the actors detail view. A simple formula allows the user to add the name and upload a file. If files exist, a list of the files appears.
It shows the information from the author, the date of upload and the name. One click on the file-symbol opens the file, one click on the shift-symbol refer to the editor formula.

Comments can be added over the "Add Comment" button to the actor.

Actor Form
----------

In the formula its important to pay attention to the form of the properties "Phone", "Mail" and "Web". Phone numbers always have to be added with a "+" and the international country code. The mail adress have
to follow the known form "@domain". The imput of a web-adress have to include the shortcuts "http://" or "https://". Over the button "Sector" multiple entries are possible.

How to assign a peron to a company?
-----------------------------------

Its basically possible to add more than one company to an employee.

In the editor formula of the person its possible to add more companies over the button "Company" every time.
