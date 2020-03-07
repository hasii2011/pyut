

𝓟 𝓨 𝓤 𝓣 stands for Python UML Tool. Actually, Pyut is only a class diagram editor


This is a Python 3 version of a source forge project.  This is the [original web site](http://pyut.sourceforge.net/whatis.html)

I asked the original developers if it was Ok to fork this project.  This is what one replied:


>> Hello,
>> 
>> This project is no longer maintained.
>> I think that you can fork this project and upgrade it depending your needs, but please keep it free ;-)
>> 
>> Good luck and keep us updated if you do the fork
>> 
>> Cédric D


So this is the fork and I let Cedric know.  

------
Note to self:

In the loggingConfiguration.json configuration file some plugin logging configuration stanzas use the fully qualified
package.className and some do not.

If we define instance loggers then we use just the class name
If we define class loggers (for parent classes) then we need the full package.className
specification
