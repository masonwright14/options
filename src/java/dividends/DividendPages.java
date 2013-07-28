package dividends;

import java.util.Arrays;
import java.util.List;

public abstract class DividendPages {

    private static final String DIVIDEND_PAGES = 
        "http://www.dividend.com/dividend-stocks/basic-materials/aluminum/aa-alcoa/,http://www.dividend.com/dividend-stocks/financial/credit-services/axp-american-express/,http://www.dividend.com/dividend-stocks/industrial-goods/aerospace-defense-major-diversified/ba-boeing-co/,http://www.dividend.com/dividend-stocks/financial/money-center-banks/bac-bank-of-america/,http://www.dividend.com/dividend-stocks/industrial-goods/farm-and-construction-machinery/cat-caterpillar-inc/,http://www.dividend.com/dividend-stocks/technology/networking-and-communication-devices/csco-cisco-systems/,http://www.dividend.com/dividend-stocks/basic-materials/major-integrated-oil-and-gas/cvx-chevron-corp/,http://www.dividend.com/dividend-stocks/basic-materials/agricultural-chemicals/dd-dupont/,http://www.dividend.com/dividend-stocks/services/entertainment-diversified/dis-the-walt-disney-company/,http://www.dividend.com/dividend-stocks/conglomerates/conglomerates-general/ge-general-electric/,http://www.dividend.com/dividend-stocks/services/home-improvement-stores/hd-home-depot/,http://www.dividend.com/dividend-stocks/technology/diversified-computer-systems/hpq-hewlett-packard/,http://www.dividend.com/dividend-stocks/technology/diversified-computer-systems/ibm-ibm-corp/,http://www.dividend.com/dividend-stocks/technology/semiconductor-broad-line/intc-intel-corp/,http://www.dividend.com/dividend-stocks/healthcare/drug-manufacturers-major/jnj-johnson-and-johnson/,http://www.dividend.com/dividend-stocks/financial/money-center-banks/jpm-jp-morgan-chase/,http://www.dividend.com/dividend-stocks/consumer-goods/beverages-soft-drinks/ko-coca-cola-co/,http://www.dividend.com/dividend-stocks/services/restaurants/mcd-mcdonalds/,http://www.dividend.com/dividend-stocks/conglomerates/conglomerates-general/mmm-3m/,http://www.dividend.com/dividend-stocks/healthcare/drug-manufacturers-major/mrk-merck/,http://www.dividend.com/dividend-stocks/technology/application-software/msft-microsoft/,http://www.dividend.com/dividend-stocks/healthcare/drug-manufacturers-major/pfe-pfizer/,http://www.dividend.com/dividend-stocks/consumer-goods/personal-products/pg-procter-and-gamble/,http://www.dividend.com/dividend-stocks/technology/telecom-services-domestic/t-atandt/,http://www.dividend.com/dividend-stocks/financial/property-and-casualty-insurance/trv-travelers-co/,http://www.dividend.com/dividend-stocks/healthcare/health-care-plans/unh-unitedhealth-group/,http://www.dividend.com/dividend-stocks/conglomerates/conglomerates-general/utx-united-technologies/,http://www.dividend.com/dividend-stocks/technology/telecom-services-domestic/vz-verizon/,http://www.dividend.com/dividend-stocks/services/discount-variety-stores/wmt-wal-mart-stores/,http://www.dividend.com/dividend-stocks/basic-materials/major-integrated-oil-and-gas/xom-exxon-mobil/";

    public static List<String> getPages() {
        return Arrays.asList(DIVIDEND_PAGES.split(","));
    }
    
    /*
    public static void main(final String[] args) {
        for (String s: getPages()) {
            System.out.println(s);
        }
    }
    */
}
