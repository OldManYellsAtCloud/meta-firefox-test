import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

langs_ltr = [
    ("ach", "Ctrl+Tab wire ikin dirica matino i kit ma ki tiyo kwedgi cokki"),
    ("af", "Ctrl+Tab besoek oortjies in die volgorde wat hulle onlangs gebruik is"),
    ("an", "Ctrl+Tab cambia de pestanya en orden d'uso mas recient"),
    ("ast", "Ctrl+Tab percuerre les llingüetes pol orde d'usu recién"),
    ("az", "Ctrl+Tab son istifadə etmə sırasına görə vərəqlər arasında dönsün"),
    ("bs", "Ctrl+Tab prolazi kroz tabove u redosljedu nedavnog korištenja"),
    ("br", "Ctrl+Tab evit mont d'an ivinell implijet da ziwezhañ"),
    ("ca", "Ctrl+Tab canvia de pestanya en ordre d'ús recent"),
    ("ca-valencia", "Ctrl+Tab canvia de pestanya en orde d'ús recent"),
    ("cy", "Mae Ctrl+Tab yn cylchdroi drwy dabiau yn y drefn y'u defnyddiwyd yn ddiweddar"),
    ("sr", "Ctrl+Tab пролази кроз картице према редоследу коришћења"),
    ("da", "Ctrl+Tabulator-tasten skifter mellem de senest anvendte faneblade"),
    ("de", "Bei Strg+Tab die Tabs nach letzter Nutzung in absteigender Reihenfolge anzeigen"),
    ("dsb", "Strg+Tab pśejźo rejtariki pó tuchylu póstajonem pórěźe"),
    ("et", "Ctrl+Tab liigub kaartide vahel viimase kasutamise järjekorras"),
    ("en-CA", "Ctrl+Tab cycles through tabs in recently used order"),
    ("en-GB", "Ctrl+Tab cycles through tabs in recently used order"),
    ("en-US", "Ctrl+Tab cycles through tabs in recently used order"),
    ("es-AR", "Ctrl+Tab rota las pestañas según su uso reciente"),
    ("es-CL", "Ctrl+Tab circula a través de las pestañas en orden según su uso reciente"),
    ("es-ES", "Ctrl+Tab pasa por las pestañas en orden de uso reciente"),
    ("es-MX", "Ctrl + Tab recorre pestañas según su uso reciente"),
    ("eo", "Stir+Tabo rondiras inter langetoj ordigitaj laŭ ĵuseco"),
    ("eu", "Ktrl+Tab konbinazioak fitxaz aldatzen du azkenekoz erabilitako ordenan"),
    ("fr", "Ctrl+Tab fait défiler vos onglets en les classant selon leur dernière utilisation"),
    ("fy-NL", "Ctrl+Tab rint troch ljepblêden yn koartlyn brûkte folchoarder"),
    ("fur", "Ctrl+Tab al fâs scori lis schedis lant daûr l'ordin di chês dopradis plui di resint"),
    ("ga-IE", "Ctrl+Tab le dul trí na cluaisíní san ord ar bhain tú úsáid astu le déanaí"),
    ("gl", "Ctrl+Tab para alternar entre as lapelas segundo o seu uso recente"),
    ("gn", "Ctrl+Tab cycles tendayke rupive eiporu ramovévape"),
    ("gd", "Cuairtichidh Ctrl+Tab thu tro na tabaichean san robh iad agad o chionn goirid"),
    ("hsb", "Strg+Tab přeběži rajtarki po tuchwilu postajenym porjedźe"),
    ("hr", "Ctrl+Tab kruži kroz kartice redoslijedom nedavnog korištenja"),
    ("id", "Ctrl+Tab berputar melalui tab dalam urutan yang baru saja digunakan"),
    ("ia", "Ctrl+Tab percurre le schedas in le ordine usate recentemente"),
    ("xh", "Imijikelo yeCtrl+Tab kwiithebhu kulungelelwano olusandul' ukusetyenziswa"),
    ("is", "Ctrl+Tab skiptir á milli flipa í notkunarröð"),
    ("it", "Scorri le schede con Ctrl+Tab ordinandole in base all’utilizzo più recente"),
    ("cak", "Ctrl+Tab mejaj pa taq ruwi' pa k'ak'a' kokisaxik kicholajem"),
    ("lv", "Ctrl+Tab slēdzas starp cilnēm to izmantošanas secībā"),
    ("lt", "Vald+Tab perjungia korteles paskiausiai naudotų eiliškumu"),
    ("lij", "Ctrl+Tab mostra l'anteprimma di feuggi averti"),
    ("hu", "A Ctrl+Tab a legutóbbi használat sorrendjében lépked körbe a lapokon"),
    ("ms", "Pusingan Ctrl+Tab mengikut tertib tab yang baru digunakan"),
    ("nl", "Ctrl+Tab doorloopt tabbladen in onlangs gebruikte volgorde"),
    ("nb-NO", "Ctrl+Tab veksler mellom faner i nylig brukt-rekkefølge"),
    ("nn-NO", "Ctrl+Tab vekslar mellom faner i nyleg brukt-rekkjefølgje"),
    ("oc", "Ctrl+Tab fa passar los onglets dins l'òrdre de darrièra utilizacion"),
    ("uz", "Ctrl+Tab yordamida varaqlarga soʻnggi foydalanish tartibida oʻtish mumkin"),
    ("pl", "Przełączanie kart za pomocą Ctrl+Tab w kolejności ostatnich wyświetleń"),
    ("pt-BR", "Ctrl+Tab alternar entre abas por ordem de uso"),
    ("pt-PT", "Ctrl+Tab permuta em ciclo os separadores pela ordem dos mais recentemente utilizados"),
    ("ff", "Ctrl+Tab yaaɓat hakkunde tabbe e deggondiral kuutoragol ɓennungol"),
    ("ro", "Ctrl+Tab parcurge filele în ordinea celor mai recent folosite"),
    ("rm", "Ctrl+Tab siglia dad in tab a l'auter en la successiun da l'ultima utilisaziun"),
    ("sc", "Ctrl+Tab cuncàmbia ischedas in s'òrdine de impreu reghente"),
    ("sco", "Ctrl+Tab gangs through tabs in the order ye last yaised them"),
    ("sq", "Ctrl+Tab ju kalon nëpër skedat sipas radhës së përdorimit së fundi"),
    ("sk", "Prepínať karty pomocou Ctrl+Tab v poradí podľa posledného otvorenia"),
    ("sl", "Ctrl+Tab kroži med zavihki po vrsti, kot so bili nazadnje uporabljeni"),
    ("son", "Ctrl+Tab willandey kanjey game goyyan kanandi koraw ra"),
    ("fi", "Ctrl+Tab selaa välilehtiä käyttöjärjestyksessä alkaen viimeisimmästä"),
    ("sv-SE", "Ctrl+Tab växlar mellan flikarna i nyligen använd ordning"),
    ("tl", "Lumipat-lipat sa mga tab gamit ang Ctrl+Tab base sa pinakahuling ginamit"),
    ("kab", "Ctrl+Tab yessezray-d accaren n umizzwer yettwasqedcen melmi kan"),
    ("vi", "Ctrl+Tab để chuyển qua các thẻ theo thứ tự sử dụng gần đây nhất"),
    ("trs", "Ctrl + Tab duguchin ma riña nej rakïj ñanj hìaj garasun'"),
    ("tr", "Ctrl+Tab, sekmeler arasında son kullanıldıkları sırayla atlasın"),
    ("cs", "Přepínat panely pomocí Ctrl+Tab v pořadí podle jejich posledního použití"),
    ("szl", "Skrōt Ctrl+Tab przełōnczo karty we raji ôd ôstatnio używanych"),
    ("el", "Εναλλαγή καρτελών με το Ctrl+Tab σε σειρά πρόσφατης χρήσης"),
    ("be", "Ctrl+Tab пераключае паміж карткамі ў парадку апошняга выкарыстання"),
    ("bg", "Ctrl+Tab обикаля разделите в реда на използване"),
    ("ru", "Ctrl+Tab переключает между вкладками в порядке недавнего использования"),
    ("tg", "Ctrl+Tab варақаҳоро аз рӯи тартиби истифодаи охирин иваз мекунад"),
    ("uk", "Перемикати вкладки натисканням Ctrl+Tab у порядку недавнього їх використання"),
    ("mk", "Ctrl+Tab преминува низ јазичињата според редоследот по кој биле користени"),
    ("kk", "Ctrl+Tab беттер арасында соңғы қолданылу реті бойынша ауысады"),
    ("hy-AM", "Ctrl+Tab՝ պտտվում է ներդիրների միջև՝ ըստ վերջին օգտագործածի"),
    ("ne-NP", "Ctrl+Tab ले हालसालै प्रयोग गरिएका ट्याबहरूमा चक्र लगाउँछ"),
    ("mr", "Ctrl+Tab वापरलेल्या क्रमामध्ये टॅब्स बदली करते"),
    ("hi-IN", "Ctrl+Tab टैब्स के द्वारा हाल ही में उपयोग किये गये अनुक्रम में घूमता है"),
    ("bn", "Ctrl+Tab সাম্প্রতিক ব্যবহৃত ট্যাবগুলোতে ক্রমান্বয়ে ঘুড়বে"),
    ("pa-IN", "ਤਾਜ਼ਾ ਵਰਤੋਂ ਦੇ ਕ੍ਰਮ ਵਿੱਚ ਟੈਬਾਂ ਵਿੱਚ ਗੇੜੇ ਲਈ Ctrl+Tab ਵਰਤੋ"),
    ("gu-IN", "તાજેતરમાં ઉપયોગમાં લેવાયેલી ક્રમમાં ટેબ દ્વારા Ctrl+Tab ચક્ર"),
    ("ta", "Ctrl+Tab விசைக் கொண்டு அண்மையில் பாவித்த கீற்றுகளின் ஊடாக வலம் வரலாம்"),
    ("te", "Ctrl+Tab ట్యాబులను వరుసగా కాకుండా వాటిని ఇటీవల వాడిన క్రమంలో చుట్టుతిప్పుతుంది"),
    ("my", "Ctrl+tab သည် အရင်သုံးခဲ့ဖူးသည့် တပ်ဗ်များကို အစဉ်လိုက် ပြောင်းပေးသွားမည်"),
    ("kn", "Ctrl+Tab ಇತ್ತೀಚೆಗೆ ಬಳಸಿದ ಟ್ಯಾಬ್‍ಗಳನ್ನು ತಿರುಗಿಕೊಡುತ್ತದೆ"),
    ("si", "Ctrl+Tab මෑතදී භාවිතා කළ අනුපිළිවෙලට පටිති සකසයි"),
    ("th", "Ctrl+Tab เพื่อสลับเปลี่ยนแท็บตามลำดับที่ใช้ล่าสุด"),
    ("ka", "Ctrl+Tab წრიულად გადართვა ჩანართებზე ბოლო გამოყენების რიგითობით."),
    ("km", "ប៊ូតុង Ctrl+Tab មានមុខងារចូលមើលផ្ទាំងដែលបើកថ្មីៗម្ដងមួយៗ"),
    ("ja", "Ctrl+Tab で最近使用した順にタブを切り替える"),
    ("zh-TW", "按下 Ctrl+Tab 時，依照最近使用分頁的順序切換分頁標籤"),
    ("zh-CN", "按下 Ctrl+Tab 时，依照最近使用顺序循环切换标签页"),
    ("ko", "Ctrl+Tab 단축키로 최근 사용한 순서대로 탭 순환")
]

langs_rtl = [
    ('he', 'Ctrl+Tab מחליף את הלשוניות לפי סדר השימוש בהן'),
    ('ur', 'Ctrl+Tab ٹہبس کے زرِیعے دورہ حالیہ اسرتعمال شدپ ترغیب میں'),
    ('ar', 'Ctrl+Tab يتنقّل عبر الألسنة حسب ترتيب آخر استخدام'),
    ('fa', 'Ctrl+Tab به ترتیب زبانه‌های اخیرا استفاده شده بین آنها حرکت می‌کند')
]

class Test_firefox:
    def start_browser(self, rtl=False):
        fp = webdriver.FirefoxProfile()
        # if RTL language is selected, start the browser
        # already with an RTL locale - otherwise, when switching
        # between RTL and LTR, the browser need to be restarted
        if rtl:
            fp.set_preference("intl.locale.requested", "he")
        fp.set_preference("extensions.installDistroAddons", True)
        fp.set_preference("extensions.autoDisableScopes", 0)
        fp.set_preference("extensions.enabledScopes", 11)
        options = Options()
        options.profile = fp
        driver = webdriver.Firefox(options = options)
        return driver

    @pytest.fixture(scope="module")
    def ltr_browser(self):
        driver = self.start_browser();
        driver.get("about:preferences")
        yield driver
        driver.quit()

    @pytest.fixture(scope="module")
    def rtl_browser(self):
        driver = self.start_browser(rtl=True)
        driver.get("about:preferences")
        yield driver
        driver.quit()

    def select_language(self, driver, language):
        languagemenu = driver.find_element(By.ID, "primaryBrowserLocale")
        languagemenu.click()
        languagepopupitems = languagemenu.find_elements(By.TAG_NAME, "menuitem")
        for item in languagepopupitems:
            if item.get_property("value") == language:
                item.click()
                languagemenu.click()
                time.sleep(5)
                return
        raise Exception("Could not find language value in list: %s" % language)


    def get_sample_sentence(self, driver):
        tabOrder = driver.find_element(By.ID, "ctrlTabRecentlyUsedOrder")
        return tabOrder.text

    def verify_displayed_sentence(self, driver, lang, expected):
        self.select_language(driver, lang)
        actual_sentence = self.get_sample_sentence(driver)
        assert expected == actual_sentence, "Language: %s failed. Expected: %s, actual: %s" % (lang, expected, actual_sentence)

    def count_available_languages(self, driver):
        languagemenu = driver.find_element(By.ID, "primaryBrowserLocale")
        languagemenu.click() # display list
        languagepopupitems = languagemenu.find_elements(By.TAG_NAME, "menuitem")
        languagemenu.click() # hide list
        return len(languagepopupitems)

    @pytest.mark.parametrize("lang, expected", langs_ltr)
    def test_ltr_languages(self, lang, expected, ltr_browser):
        self.verify_displayed_sentence(ltr_browser, lang, expected)

    @pytest.mark.parametrize("lang, expected", langs_rtl)
    def test_rtl_languages(self, lang, expected, rtl_browser):
        self.verify_displayed_sentence(rtl_browser, lang, expected)

    def test_count_languages(self, ltr_browser):
        expected_num_of_languages = len(langs_ltr) + len(langs_rtl) + 1 # +1 is the "get new languages..." option
        actual_num_of_languages = self.count_available_languages(ltr_browser)
        assert expected_num_of_languages == actual_num_of_languages, "Incorrect language count. \
               Expected: %d, actual: %d" % (expected_num_of_languages, actual_num_of_languages)
