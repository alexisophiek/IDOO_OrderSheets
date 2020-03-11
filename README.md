# IDOO OrderSheet Generator
Automated Order Sheet App.  For the purpose of calculating orders per store in each Market based on each markets allocation. Requires separate IDOO Login to review allocations and input those numbers.  Note: Allocations cannot be NULL, must be zero.

### Still in Development

JupyterNotebook will perform chrome driver navigation of online POS reporting system, download file for a single market, load the most recent file in pre-set download path.  Once loaded, using pandas, a series of cleaning and munging will take place.  User will be asked to input the quantities of device allocation the Company.  This can be accessed through each Markets T-Mobile Ordering Portal. 

Recent Update:

Notebook now includes columns for stores total inventory minus Sim Cards and DEMO skus.  Also includes another column which calculates percent of a given device of that stores total inventory.  The goal is to encourage store's to "Smart Sell" even when a promo is hot.  A store should never have one device be more than a total percentage of their inventory.  What that threshold is- is TBD.

Goals:
Add to a framework server for internal tools for the Audit Team.

