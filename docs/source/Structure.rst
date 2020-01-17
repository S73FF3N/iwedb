Structure
=========

The Success Map is devided in 6 categories, which form the logical structure:
Turbine Models, Actors, Wind Farms, Turbines, Projects and Contracts.


Every category form, in connection with its charakteristically properties, a
logical unit. Over the defination of the properties, objects of the different
categories can be created and saved in the databases. The following examples
discribe this precept.

Object: Senvion 3.2M114
-----------------------

    -   Category: Turbine Model
    -   Property: Manufacturer = "Senvion"
    -   Property: Name = "3.2M114"
    -   Property: Performance = 3200kW
    -   ...

The object Senvion 3.2M114 of the category Turbine Model got definated
completely by a few properties (Manufacturer, Name, Performance and so on).
In comparison this is how a object of the category Wind Farm looks like:

Object: Buchonia
----------------

    -   Category: Wind Farm
    -   Property: Name = "Buchonia"
    -   Property: Country = "Germany"
    -   Property: Place = "Schlüchtern"
    -   ...

A Wind Farm object has other properties than a Turbine Model object:
Name, Country, Place and so on.

In general there are 3 views for each category. First there is a list view,
which shows all usable objects of a categroy and gives the option to do
individual selection. Also ther is a detail view, which shows the diefferent
properies of an object. At last, the formula view gives the possibility to
add new objects and edit already existing objects.

The categories going to be discribed in detail in the other parts.

