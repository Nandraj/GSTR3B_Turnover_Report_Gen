# GSTR-3B Turnover Report Generator [2019-20]

![GSTR-3B T/o report gen view](3b_turnover_report_gen.jpg?raw=true "NR GSTR-3B Turnover Report Generator")

It helps in generating 2019-20 GSTR-3B turnover report which includes all data of Table 3.1 which can be used for deciding total turnover for the year or to match with account for annual return preparation.

### System requirement
- Windows 7(with service pack 1) or later
- Google chrome browser

### How to Use window binary ?
1. Download binary and excel template from this [link](https://app.box.com/s/locmnk8a7kmbg0srrh3ztrddmuq4ndam)

2. Put excel file at appropriate location and paste your client data into it

3. Extract .rar file containing software to run .exe file within extracted folder.

4. Start software.

5. [For first time only] Select excel file and press "Generate DB" button. database file with same name as of excel got generated and its path is filled up in second input box. Now press "Start Processing" button.

6. [For second time and later] For second input box browse and select database file generated first time and press "Start Processing" button

If you select excel file in second time or later all previous data stored in database will gets deleted, so be cautious.

7. Popup will open for captcha entry. You can minimize and chill until second popup get opened.

8. At the end of processing you will get 2 csv file. check for client csv file where last column is for processing status if there are some "no" against clients then re run software > select database file and go ahead for second processing so that processed status changed to "yes".

9. Checkout gstr3b data csv file which has all month sales data for all clients given in template when you processed it for the first time.

10. Though once all client data got saved csv reports are automatically gets generated but if you wish to generate it manually then select database file and press Generate Reports button.

*chromedriver matching with your pc's chrome is required in NR GST Auto folder. You can check your chrome version by going to Help > About google chrome. You can download chromedriver from this [link](https://chromedriver.chromium.org/downloads)