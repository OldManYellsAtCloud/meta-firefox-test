import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

langs = [
    ("ach", "Pot buk man tye ki ngec matek me tic cing ma pire twero bedo tek ka itye ka temo cobo peko. Ka ce itye kamoyo pi lagam me lapeny ma ngene ikom Firefox, rot support web site."),
    ("af", "Hierdie bladsy bevat tegniese inligting wat nuttig kan wees wanneer u 'n probleem probeer oplos. Indien u soek vir antwoorde op algemene vrae oor Firefox, besoek gerus ons steunwerf."),
    ("an", "Ista pachina contiene información tecnica que puede estar util quan prebe de resolver un problema. Si ye buscando respuestas a preguntas freqüents sobre Firefox, mire o puesto d'asistencia."),
    ("ast", "Esta páxina contién información téunica que pue ser útil cuando tentes d'iguar un problema. Si busques rempuestes a entrugues frecuentes tocante a Firefox, visita'l nuesu sitiu web de sofitu."),
    ("az", "Bu səhifə, bir problemi həll etməyə çalışarkən işinizə yaraya biləcək texniki məlumatlara malikdir. Firefox haqqında ümumi suallarla bağlı cavab axtarırsınızsa dəstək saytımıza baxın."),
    ("bs", "Ova stranica sadrži tehničke informacije koje vam mogu biti korisne kada pokušavate riješiti problem. Ukoliko tražite odgovore na često postavljena pitanja o Firefoxu, posjetite našu web stranicu za podršku."),
    ("br", "Ar bajenn-mañ a endalc'h stlennoù teknikel hag a c'hallfe bezañ talvoudus pa glaskit  dirouestlañ ur gudenn. Mar klaskit respontoù da c'houlennoù boutin a-zivout  Firefox, e c'hallit klask war hol lec'hienn skoazell."),
    ("ca", "Aquesta pàgina conté informació tècnica que pot ser útil quan proveu de resoldre un problema. Si cerqueu respostes per a preguntes freqüents del Firefox, visiteu el nostre lloc web d'assistència."),
    ("ca-valencia", "Esta pàgina conté informació tècnica que pot ser útil quan proveu de resoldre un problema. Si cerqueu respostes per a preguntes freqüents del Firefox, visiteu el nostre lloc web d'assistència."),
    ("cy", "Mae'r dudalen hon yn cynnwys gwybodaeth dechnegol a allai fod yn ddefnyddiol pan fyddwch yn ceisio datrys problem. Os ydych yn chwilio am atebion i gwestiynau cyffredin am Firefox, edrychwch ar ein gwefan cefnogaeth."),
    ("sr", "Ова страница садржи техничке податке који могу бити корисни када покушавате да решите неки проблем. Ако вам требају одговори на често постављана питања о програму Firefox, прегледајте наш веб сајт за подршку."),
    ("da", "Denne side indeholder teknisk information som måske kan være brugbar når du forsøger at løse et problem. Hvis du leder efter svar på ofte spurgte spørgsmål om Firefox, kan du besøge vores supportwebsted"),
    ("de", "Diese Seite enthält technische Informationen, die nützlich sein könnten, wenn Sie versuchen, ein Problem zu lösen. Wenn Sie nach Antworten auf häufig gestellte Fragen zu Firefox suchen, besuchen Sie bitte unsere Hilfeseite."),
    ("dsb", "Toś ten bok wopśimujo techniske informacije, kótarež by mógli wužytne byś, gaž wopytujośo problem rozwězaś. Jolic pytaśo za wótegronami za zwucone pšašanja wó Firefox, woglědajśo se k našomu websedłoju pódpěry."),
    ("et", "See leht sisaldab tehnilist teavet, mis võib olla kasulik probleemide lahendamisel. Kui otsid vastuseid Firefoxi puudutavatele enamlevinud küsimustele, siis külasta meie tugiveebi."),
    ("en-CA", "This page contains technical information that might be useful when you’re trying to solve a problem. If you are looking for answers to common questions about Firefox, check out our support website."),
    ("en-GB", "This page contains technical information that might be useful when you’re trying to solve a problem. If you are looking for answers to common questions about Firefox, check out our support web site."),
    ("en-US", "This page contains technical information that might be useful when you’re trying to solve a problem. If you are looking for answers to common questions about Firefox, check out our support website."),
    ("es-AR", "Esta página contiene información técnica que podría ser útil si está tratando de resolver un problema. Si está buscando respuestas a preguntas comunes acerca de Firefox, busque en el sitio web de soporte."),
    ("es-CL", "Esta página contiene información técnica que puede serle útil cuando intente resolver un problema. Si está buscando respuestas a preguntas comunes acerca de Firefox, mire en nuestro sitio web de soporte."),
    ("es-ES", "Esta página contiene información técnica que puede ser útil cuando intente solucionar un problema. Si está buscando respuestas a preguntas frecuentes sobre Firefox, visite nuestro sitio de asistencia."),
    ("es-MX", "Esta página presenta información técnica que puede ser de ayuda si necesitas resolver un problema. Para obtener respuestas a preguntas comunes sobre Firefox visita nuestro sitio web de soporte."),
    ("eo", "Tiu ĉi paĝo enhavas teknikajn informojn kiuj povas esti utilaj kiam vi klopodas solvi problemon. Se vi serĉas respondojn al oftaj demandoj pri Firefox, bonvolu viziti nian helporetejon."),
    ("eu", "Orri honek arazo bat konpontzeko erabilgarria izan daitekeen informazio teknikoa du. Firefox(r)i buruzko ohiko galderen erantzunen bila bazabiltza, bisitatu gure laguntzaren webgunea."),
    ("fr", "Cette page contient des informations techniques qui pourraient être utiles quand vous essayez de résoudre un problème. Si vous cherchez des réponses à des questions courantes sur Firefox, veuillez consulter notre site web d’assistance."),
    ("fy-NL", "Dizze side befettet technyske ynformaasje dy’t brûkber wêze kin as jo probearje om problemen op te lossen. As jo antwurden sykje op algemiene fragen oer Firefox, sjoch dan op ús stipewebsite."),
    ("fur", "Cheste pagjine e conten informazions tecnichis che a podaressin risultâ utilis par cirî di risolvi problemis. Se tu sês daûr a cirî rispuestis aes domandis plui frecuentis su Firefox, da une cjalade al nestri sît web di supuart."),
    ("ga-IE", "Ar an leathanach seo tá eolas teicniúil a d'fhéadfadh a bheith úsáideach agus tú ag iarraidh fadhb a réiteach. Má tá freagraí á lorg agat ar cheisteanna coitianta maidir le Firefox, féach ar ár suíomh tacaíochta."),
    ("gl", "Esta páxina contén información técnica que pode serlle útil cando tente solucionar un problema. Se está buscando respostas a preguntas frecuentes sobre o Firefox, visite o noso sitio web de asistencia."),
    ("gn", "Ko kuatiarogue oguereko marandu aporekoguáva ikatúva eiporu emyatyrõse jave peteĩ apañuái. Ehekáramo mbohovái umi porandu oikovéva Firefox rehegua, eike tenda eikekuaaha."),
    ("gd", "Tha fiosrachadh teicnigeach air an duilleag seo a dh'fhaodadh a bhith feumail dhut ann am fuasgladh dhuilgheadasan. Ma tha ceist neo-theicnigeach agad mu Firefox, cuir sùil air an làrach-taice againn."),
    ("hsb", "Tuta strona wobsahuje techniske informacije, kotrež móhli wužitne być, hdyž pospytujeće problem rozrisać. Jeli za wotmołwami za zwučene prašenja wo Firefox pytaće, wopytajće našu podpěranske websydło."),
    ("hr", "Ova stranica sadrži tehničke podatke koji mogu biti korisni pri rješavanju problema. Ako tražiš odgovore na česta pitanja o Firefoxu, posjeti našu web stranicu podrške."),
    ("id", "Laman ini berisi informasi teknis yang mungkin berguna ketika Anda berusaha mengatasi masalah. Jika Anda mencari jawaban untuk pertanyaan umum tentang Firefox, silakan kunjungi situs web layanan dukungan kami."),
    ("ia", "Iste pagina contine informationes technic que pote servir quando tu tenta de resolver un problema. Si tu cerca responsas a questiones commun re Firefox, controla nostre sito web de assistentia."),
    ("xh", "Eli phepha liqulethe inkcazelo yobuchwepheshe enokuba luncedo xa uzama ukusombulula ingxaki. Ukuba ufuna iimpendulo kwimibuzo eqhelekileyo ye-Firefox, khangela kwisayithi yethu support website."),
    ("is", "Þessi síða inniheldur tæknilegar upplýsingar sem gætu verið hjálplegar ef þú ert að reyna að leysa eitthvað vandamál. Ef þú ert að leita að svörum við algengum spurningum um Firefox, athugaðu þá hjálparvefsvæðið okkar."),
    ("it", "Questa pagina contiene informazioni tecniche che potrebbero risultare utili per risolvere eventuali problemi. Per le risposte alle domande più comuni a proposito di Firefox, consultare il sito web dedicato al supporto."),
    ("cak", "Pa re ruxaq re' k'o samajel etamab'äl chupam, ri nito'on we nawajo' nasöl jun k'ayewal. Richin nawïl kitzijol relik taq k'utunïk chi rij Firefox, kab'etz'eton pa qa ruxaq k'amaya'l richin to'ïk."),
    ("lv", "Šī lapa satur tehnisku informāciju, kas var būt noderīga, mēģinot novērst problēmu. Ja meklējat atbildes uz vienkāršiem jautājumiem par Firefox, aplūkojiet mūsu atbalsta mājas lapu."),
    ("lt", "Šiame tinklalapyje rasite visą techninę informaciją, kuri gali praversti sprendžiant su „Firefox“ iškilusias problemas. Jei ieškote atsakymų į dažniausius klausimus apie šią programą, apsilankykite pagalbos svetainėje."),
    ("lij", "Sta pagina a contegne informaçioin tecniche che peuan ese utili quande ti preuvi a risòlve un problema. Se ti çerchi rispòste a domande comuni in sce Firefox, contròlla o nòstro scito de agiutto."),
    ("hu", "Ez az oldal problémakeresésnél használható technikai információkat tartalmaz. Ha a Firefox programmal kapcsolatos gyakori kérdésekre keresi a választ, akkor nézze meg a támogató weboldalunkat."),
    ("ms", "Halaman ini mengandungi maklumat teknikal yang mungkin berguna apabila anda cuba menyelesaikan masalah. Jika anda mencari jawapan soalan lazim berkenaan Firefox, semak di support website."),
    ("nl", "Deze pagina bevat technische informatie die handig kan zijn als u een probleem probeert op te lossen. Als u antwoorden op veelgestelde vragen over Firefox zoekt, kijk dan op onze ondersteuningswebsite."),
    ("nb-NO", "Denne siden inneholder teknisk informasjon som kan være nyttig når du forsøker å løse et problem. Besøk også brukerstøttenettstedet for å få svar på ofte stilte spørsmål om Firefox."),
    ("nn-NO", "Denne sida inneheld teknisk informasjon som kan vere nyttig når du prøver å løyse eit problem. Gå til brukarstøttenettsida for å få svar på ofte stilte spørsmål om Firefox."),
    ("oc", "Aquesta pagina conten d'informacions tecnicas que poirián èsser utilas quand ensajatz de resòlvre un problèma. Se cercatz de responsas a de questions correntas sus Firefox, consultatz nòstre site Web d'assisténcia."),
    ("uz", "Bu sahifa muammolarni hal qilishingizda foydasi tegishi mumkin bo‘lgan texnik ma’lumotlarga ega. Agar siz Firefox haqida umumiy savollarga javob izlayotgan bo‘lsangiz, bizning yordam saytimiznitekshirib ko‘ring."),
    ("pl", "Ta strona zawiera informacje techniczne, które mogą być przydatne podczas rozwiązywania problemów. Jeśli szukasz odpowiedzi na często zadawane pytania dotyczące programu Firefox, sprawdź naszą stronę wsparcia technicznego."),
    ("pt-BR", "Esta página contém informações técnicas que podem ser úteis se você estiver tentando solucionar um problema. Se estiver procurando respostas às dúvidas mais comuns sobre o Firefox, consulte o site de suporte."),
    ("pt-PT", "Esta página contém informação técnica que pode ser útil para quando estiver a tentar resolver um problema. Se estiver à procura de respostas a questões comuns acerca do Firefox, aceda ao nosso site de apoio."),
    ("ff", "Ngoo hello ena waɗi humpito karallaagal baawngol nafde so aɗaetoo safrude caɗeele. So aɗa yiyloo jaabawuuji naamne ganndaaɗe baɗte Firefox, ƴeewto wallitorde amen lowre wallitorde."),
    ("ro", "Această pagină conține informații tehnice care ar putea fi utile atunci când încerci să rezolvi o problemă. Dacă cauți răspunsuri la întrebări comune despre Firefox, verifică site-ul nostru de suport."),
    ("rm", "Questa pagina cuntegna infurmaziuns tecnicas che pudessan esser nizzaivlas, sche ti emprovas da schliar in problem. Sche ti tschertgas respostas a dumondas frequentas davart Firefox, visita per plaschair nossa pagina d'agid."),
    ("sc", "Custa pàgina cuntenet informatziones tècnicas chi ti podent torrare ùtiles cando ses chirchende de acontzare unu problema. Si ses chirchende rispostas a preguntas fitianas in pitzus de Firefox, càstia su situ web de agiudunostru."),
    ("sco", "This page conteens technical information that micht be yaisefu whan yer ettlin at solvin a problem. Gin yer luikin fur answers tae common speirins aboot Firefox, hae a glisk at oor support website."),
    ("sq", "Kjo faqe përmban të dhëna teknike që mund të jenë të dobishme, kur përpiqeni të zgjidhni një problem. Nëse po shihni për përgjigje për pyetje të rëndomta rreth Firefox-it, shihni te sajti ynë i asistencës."),
    ("sk", "Táto stránka obsahuje technické informácie, ktoré môžu byť užitočné pri riešení problémov s touto aplikáciou. Ak hľadáte odpovede na bežné otázky o programe Firefox, navštívte stránku podpory."),
    ("sl", "Ta stran vsebuje tehnične podatke, ki jih boste morda potrebovali pri odpravljanju težav. Če iščete odgovore na splošna vprašanja o programu Firefox, obiščite strani za podporo uporabnikom."),
    ("son", "Moɲoo woo goo nda goyandi alhabar kaŋ ga hin ka bara nda nafaw waati kaŋ war ga ceeci ka fatta šenday ra. Nda war ga zaabiyaŋ ceeci war zaarikul hãayaney se Firefox ga, ir faaba Interneti nungoo guna."),
    ("fi", "Tällä sivulla on teknisiä tietoja, jotka voivat olla avuksi kun yritetään ratkaista jotain ongelmaa ohjelman kanssa. Jos olet etsimässä vastauksia kysymyksiin Firefoxista, käy katsomassa löytyykö hakemaasi vastausta tukisivustoltamme."),
    ("sv-SE", "Den här sidan innehåller teknisk information som kan vara till hjälp när du försöker lösa ett problem. Vill du se svaren på några av de vanligaste frågorna om Firefox, kan du besöka vår supportwebbplats."),
    ("tl", "Ang pahinang ito ay naglalaman ng teknikal na impormasyon na maaaring makatulong kapag may sinusubukan kang ayusin na problema. Kung naghahanap ka ng kasagutan sa mga karaniwang katanungan tungkol sa Firefox, bisitahin ang ating support website."),
    ("kab", "Asebter-agi igber talɣut tatiknikant i izemren ahat ticki tettaɛraḍeḍ ad tefruḍ ugur. Ma yella tettnadiḍ tiririt ɣef isteqsiyen n Firefox,senqed asmel-nneɣ Web."),
    ("vi", "Trang này chứa thông tin kĩ thuật có thể có ích khi bạn đang cố giải quyết một vấn đề. Nếu bạn đang tìm câu trả lời cho các câu hỏi thông thường về Firefox, hãy xem trang web hỗ trợ của chúng tôi."),
    ("trs", "Ñuna narit nuguan'an rayi'i sa na'ue gi'iaj sun hue'e riña aga' na. Sisi na'na'ui' nuinsaj hua sa hua danaj riña Firefox, ga'ue ni'iaj riña na da' rugujñu'un so'."),
    ("tr", "Bu sayfa, bir sorunu gidermeye çalışırken işinize yarayabilecek teknik bilgiler içerir. Firefox hakkında genel sorularla ilgili yanıt arıyorsanız destek sitemizi ziyaret edin."),
    ("cs", "Tato stránka obsahuje technické informace, které mohou být užitečné, pokud se snažíte vyřešit nějaký složitější problém s aplikací. Odpovědi na často kladené otázky ohledně Firefoxu naleznete na webových stránkách podpory."),
    ("szl", "Na tyj strōnie znojdziesz techniczne informacyje, kere mogōm sie przidać, jak mosz problym do rozwiōnzanio. Jak szukosz za ôdpowiydziami na pytania ô aplikacyjo Firefox, co sōm porzōnd zadowane, badnij na nasza strōna spōmożki."),
    ("el", "Αυτή η σελίδα περιέχει τεχνικές πληροφορίες που ενδέχεται να φανούν χρήσιμες κατά την επίλυση προβλημάτων. Αν ψάχνετε για απαντήσεις σε συχνές ερωτήσεις σχετικά με το Firefox, δείτε τη σελίδα υποστήριξής μας."),
    ("be", "Гэта старонка змяшчае тэхнічныя звесткі, якія могуць быць карыснымі, калі спрабуеце вырашыць праблему. Калі вы шукаеце адказы на агульныя пытанні пра Firefox, наведайце наш сайт падтрымкі."),
    ("bg", "Тази страница съдържа техническа информация, която може да ви е от полза, когато се опитвате да решите проблем. Ако търсите отговори на често задавани въпроси за Firefox, проверете в нашата страница за поддръжка."),
    ("ru", "Эта страница содержит техническую информацию, которая может быть полезна, когда вы пытаетесь решить проблему. Если вы ищете ответы на типичные вопросы о Firefox, обратитесь на наш веб-сайт поддержки."),
    ("tg", "Ин саҳифа дорои маълумоти техникӣ мебошад, ки ҳангоми кӯшиши ислоҳкунии мушкилӣ метавонад кумак расонад. Агар шумо ба саволҳои умумӣ дар бораи «Firefox» ҷавобҳоро ҷустуҷӯ кунед, ба сомонаи дастгирии мо ворид шавед."),
    ("uk", "Ця сторінка містить технічну інформацію, що може стати в пригоді під час усунення проблем. Якщо ж вам потрібні відповіді на поширені питання про Firefox, відвідайте наш сайт підтримки."),
    ("mk", "Оваа страна содржи технички информации кои може да Ви послужат кога се обидувате да решите некој проблем. Ако барате одговори на често поставувани прашања за Firefox, појдете на нашиот веб сајт за поддршка."),
    ("kk", "Бұл парақта мәселелерді шешуде пайдалы бола алатын техникалық ақпарат бар. Егер сіз Firefox туралы жалпы сұрақтарға жауапты іздесеңіз, біздің қолдау көрсету сайтын шолыңыз."),
    ("hy-AM", "Այս էջը պարունակում է տեխնիկական ինֆորմացիա, որը կարող է օգտակար լինել, երբ դուք փորձում եք լուծել խնդիրը:Եթե դուք փնտրում եք Firefox-ին վերաբերող ընդհանուր հարցերին պատասխաններ,փորձեք մեր աջակցող կայքը :"),
    ("ne-NP", "This page contains technical information that might be useful when you're trying to solve a problem. If you are looking for answers to common questions about Firefox, check out our support web site."),
    ("mr", "This page contains technical information that might be useful when you're trying to solve a problem. If you are looking for answers to common questions about Firefox, check out our support web site."),
    ("hi-IN", "यह पृष्ठ आपको एक समस्या को हल करने की कोशिश कर रहे हैं उपयोगी हो सकता है कि तकनीकी जानकारी है. Firefox, के बारे में आम सवालों के जवाब की तलाश में हैं, हमारे समर्थन वेबसाइट की जाँच करें."),
    ("bn", "এ পাতায় প্রযুক্তিগত তথ্য আছে যা সমস্যা সমাধানের সময় আপনার জন্য উপকারী হতে পারে। আপনি যদি Firefox সম্পর্কিত কোনো সাধারণ প্রশ্নের উত্তর খুঁজতে থাকেন, তবে আমাদের সহায়তা ওয়েবসাইট দেখুন।"),
    ("pa-IN", "ਇਹ ਸਫ਼ੇ ਉੱਤੇ ਤਕਨੀਕੀ ਜਾਣਕਾਰੀ ਹੈ, ਜੋ ਕਿ ਤੁਹਾਨੂੰ ਸਮੱਸਿਆ ਹੱਲ਼ ਕਰਨ ਲਈ ਫਾਇਦੇਮੰਦ ਹੋ ਸਕਦੀ ਹੈ। ਜੇ ਤੁਸੀਂ Firefox ਬਾਰੇ ਆਮ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਲੱਭ ਰਹੇ ਹੋ ਤਾਂ ਸਾਡੀ ਸਪੋਰਟ ਵੈੱਬ ਸਾਈਟ ਨੂੰ ਵੇਖੋ ਜੀ।"),
    ("gu-IN", "આ પાનું ટૅકનિકલ જાણકારીને સમાવે છે કે જે ઉપયોગી થઇ શકે છે જ્યારે તમે સમસ્યાનો ઉકેલ લાવવાનો પ્રયત્ન કરી રહ્યા હોય. જો તમે Firefox વિશે સામાન્ય પ્રશ્ર્નોનાં જવાબો જોઇ રહ્યા હોય, અમારી આધાર વેબ સાઇટ ને ચકાસો."),
    ("ta", "இந்த பக்கமானது ஒரு பிரச்சனைக்கு தீர்வு காணும் பொருட்டு தேவைப்படும் நுட்ப தகவல்களை கொண்டிருக்கலாம். ஒருவேளை தாங்கள் பொதுவான பதிலுக்கு எதிர்பார்த்தால் Firefox பற்றிய, எங்களின் பக்கத்தை பாருங்கள் இணையத்தள உதவி."),
    ("te", "మీరు ఒక సమస్యను పరిష్కరించుటకు ప్రయత్నించునప్పుడు మీకు ఉపయోగవంతంగా వుండగల సాంకేతిక సమాచారమును ఈ పేజీ కలిగివుంటుంది. మీరు Firefox గురించిన వుమ్మడి ప్రశ్నలకు సమాధానముల కొరకు చూస్తుంటే, మా తోడ్పాటు వెబ్ సైట్ చూడండి."),
    ("my", "This page contains technical information that might be useful when you're trying to solve a problem. If you are looking for answers to common questions about Firefox, check out our support website."),
    ("kn", "ನೀವು ಒಂದು ಸಮಸ್ಯೆಗೆ ಪರಿಹಾರ ಹುಡುಕುವಾಗ ನಿಮಗೆ ನೆರವಾಗುವಂತಹ ಮಾಹಿತಿಗಳನ್ನು ಈ ಪುಟವು ಹೊಂದಿರುತ್ತದೆ. ನೀವು Firefox ಕುರಿತಾದ ಸಾಮಾನ್ಯವಾದ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರವನ್ನು ಹುಡುಕುತ್ತಿದ್ದಲ್ಲಿ, ಬೆಂಬಲ ಜಾಲ ತಾಣವನ್ನು ನೋಡಿ."),
    ("si", "ඔබ ගැටලුවක් විසඳීමට උත්සාහ කරමින් සිටින විට ප්‍රයෝජනවත් විය හැකි තාක්‍ෂණික තොරතුරු මෙම පිටුවෙහි අඩංගු වේ. Firefox ගැන සරල ප්‍රශ්නවලට පිළිතුරු සොයන්නේ නම්, අපගේ සහාය අඩවිය බලන්න."),
    ("th", "หน้านี้มีข้อมูลทางเทคนิคที่อาจเป็นประโยชน์เมื่อคุณกำลังพยายามแก้ไขปัญหา หากคุณกำลังมองหาคำตอบสำหรับคำถามที่พบบ่อยเกี่ยวกับ Firefox ตรวจสอบ เว็บไซต์สนับสนุน ของเรา"),
    ("ka", "ეს გვერდი შეიცავს ტექნიკურ მონაცემებს, რომლებიც შესაძლოა, წარმოქმნილი ხარვეზის მოგვარებაში დაგეხმაროთ. თუ ხშირად დასმულ საკითხებზე ეძებთ პასუხს, რომლითაც შეგეძლებათ გამართოთ Firefox, იხილეთ ჩვენი მხარდაჭერის გვერდი."),
    ("km", "ទំព័រនេះ មានព័ត៌មានបច្ចេកទេសដែលអាចមានប្រយោជន៍ នៅពេលដែលអ្នក ព្យាយាមដោះស្រាយបញ្ហា ។ ប្រសិនបើអ្នកកំពុងរកចម្លើយសម្រាប់សំណួរទូទៅ អំពី Firefox ពិនិត្យមើល តំបន់បណ្ដាញគាំទ្រ របស់យើង ។"),
    ("ja", "このページには問題発生時に役立てられる技術情報が表示されます。Firefox に関する一般的な質問については サポートサイト をご覧ください。"),
    ("zh-TW", "此頁面包含可能可以幫您解決問題的技術資訊。如果您正在尋找關於 Firefox 的常見問題，請看看我們的技術支援站。"),
    ("zh-CN", "本页面包含的技术信息在您寻求解决方法时或许能帮上忙。 如果您正在寻找 Firefox 常见问题的答案， 可以查阅我们的帮助网站。"),
    ("ko", "이 페이지에는 문제 해결에 유용한 기술 정보가 포함되어 있습니다. Firefox의 일반적인 질문에 대한 답변은 지원 웹 사이트를 확인하세요."),
    ('he', 'דף זה מכיל מידע טכני שאולי שימושי עבורך כשתנסה לפתור בעיות. אם אתה מחפש תשובות לשאלות נפוצות על Firefox, עבור לאתר התמיכה.'),
    ('ur', 'اس صفحے کو آپ ایک مسئلہ کو حل کرنے کی کوشش کر رہے ہیں جب مفید ہو سکتا ہے کہ تکنیکی معلومات پر مشتمل ہے. آپ Firefox, بارے میں عمومی سوالات کے جوابات کے لئے تلاش کر رہے ہیں تو ؛، ہمارے حمایت کی ویب سائٹ کو چیک کریں.'),
    ('ar', 'تحتوي هذه الصفحة معلومات تقنية قد تكون مفيدة عندما تحاول حل مشكلة ما. إن كنت تبحث عن إجابات لأسئلة شائعة تخص Firefox، تحقق من موقع الدعم.'),
    ('fa', 'این صفحه حاوی اطلاعات فنی است که امکان دارد هنگامی که به دنبال حل مشکلی هستید به شما کمک کند. اگر به دنبال پاسخی برای پرسش‌های معمول دربارهٔ Firefox هستید، از وبگاه پشتیبانی ما بازدید نمایید.')
]

class Test_firefox:
    def start_browser(self, lang):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.locale.requested", lang)
        fp.set_preference("extensions.installDistroAddons", True)
        fp.set_preference("extensions.autoDisableScopes", 0)
        fp.set_preference("extensions.enabledScopes", 11)
        options = Options()
        options.profile = fp
        driver = webdriver.Firefox(options = options)
        return driver

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
        assert actual_sentence.startswith(expected), "Language: %s failed. Expected: %s, actual: %s" % (lang, expected, actual_sentence)

    def count_available_languages(self, driver):
        languagemenu = driver.find_element(By.ID, "primaryBrowserLocale")
        languagemenu.click() # display list
        languagepopupitems = languagemenu.find_elements(By.TAG_NAME, "menuitem")
        languagemenu.click() # hide list
        return len(languagepopupitems)

    @pytest.mark.parametrize("lang, expected", langs)
    def test_languages(self, lang, expected):
        driver = self.start_browser(lang)
        driver.get("about:support")
        actual_text = driver.find_elements(By.CLASS_NAME, "page-subtitle")[0].text
        driver.quit()
        assert actual_text == expected

