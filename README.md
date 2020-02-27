# IDOO OrderSheet Generator
Automated Order Sheet App.  For the purpose of calculating orders per store in each Market based on each markets allocation.

### Still in Development

JupyterNotebook will perform chrome driver navigation of online POS reporting systemm, download most file for a single market, load the most recent file in pre-set download path.  Once loaded, using pandas, a series of cleaning and munging will take place.  User will be asked to input the quantities allocation the Company within that Market's IDOO Portal. 

Final DF still needs orderqty and request columns formatted, labelled and rounded to the nearest five.  Final Export should also include colored columns.
