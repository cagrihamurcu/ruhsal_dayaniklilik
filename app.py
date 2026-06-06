import streamlit as st
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Yetişkinler İçin Ruhsal Dayanıklılık Ölçeği",
    page_icon="🧭",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 20px !important;
}
.main .block-container {
    max-width: 1050px;
    padding-top: 2rem;
}
h1 {
    font-size: 2.5rem !important;
}
h2, h3 {
    font-size: 1.8rem !important;
}
p, li, div, span, label {
    font-size: 1.14rem !important;
    line-height: 1.55 !important;
}
.stCaptionContainer, .stCaptionContainer p {
    font-size: 1.18rem !important;
}
.stRadio label, .stRadio div, .stRadio span, .stRadio p {
    font-size: 1.24rem !important;
}
div[role="radiogroup"] label p {
    font-size: 1.28rem !important;
    font-weight: 650 !important;
}
.stButton button, .stDownloadButton button {
    font-size: 1.12rem !important;
    padding: 0.7rem 1.05rem !important;
}
.question-box {
    background-color:#f7f7f9;
    border:1px solid #e2e2e8;
    border-radius:16px;
    padding:22px 24px;
    margin-top:12px;
    margin-bottom:14px;
}
.question-title {
    font-size:1.42rem !important;
    font-weight:750;
    margin-bottom:12px;
}
.anchor-text {
    font-size:1.26rem !important;
    color:#333;
    margin-bottom:8px;
}
.scale-help {
    font-size:1.13rem !important;
    color:#555;
    margin-top:10px;
}
.report-box {
    background-color:#fbfbfd;
    border-left:6px solid #b8b8c8;
    padding:22px 24px;
    border-radius:12px;
    margin:14px 0 22px 0;
}
.report-box p, .report-box div, .report-box strong {
    font-size:1.15rem !important;
}
</style>
""", unsafe_allow_html=True)


ITEMS = [
    {"no": 1, "text": "Beklenmedik bir olay olduğunda…", "left": "Her zaman bir çözüm bulurum", "right": "Çoğu kez ne yapacağımı kestiremem", "high": "left", "subscale": "Kendilik algısı"},
    {"no": 2, "text": "Gelecek için yaptığım planların…", "left": "Başarılması zordur", "right": "Başarılması mümkündür", "high": "right", "subscale": "Gelecek algısı"},
    {"no": 3, "text": "En iyi olduğum durumlar şu durumlardır…", "left": "Ulaşmak istediğim açık bir hedefim olduğunda", "right": "Tam bir günlük boş bir vaktim olduğunda", "high": "left", "subscale": "Yapısal stil"},
    {"no": 4, "text": "…olmaktan hoşlanıyorum", "left": "Diğer kişilerle birlikte", "right": "Kendi başıma", "high": "left", "subscale": "Sosyal yeterlilik"},
    {"no": 5, "text": "Ailemin, hayatta neyin önemli olduğu konusundaki anlayışı…", "left": "Benimkinden farklıdır", "right": "Benimkiyle aynıdır", "high": "right", "subscale": "Aile uyumu"},
    {"no": 6, "text": "Kişisel konuları…", "left": "Hiç kimseyle tartışmam", "right": "Arkadaşlarımla / aile üyeleriyle tartışabilirim", "high": "right", "subscale": "Sosyal kaynaklar"},
    {"no": 7, "text": "Kişisel problemlerimi…", "left": "Çözemem", "right": "Nasıl çözebileceğimi bilirim", "high": "right", "subscale": "Kendilik algısı"},
    {"no": 8, "text": "Gelecekteki hedeflerimi…", "left": "Nasıl başaracağımı bilirim", "right": "Nasıl başaracağımdan emin değilim", "high": "left", "subscale": "Gelecek algısı"},
    {"no": 9, "text": "Yeni bir işe / projeye başladığımda…", "left": "İleriye dönük planlama yapmam, derhal işe başlarım", "right": "Ayrıntılı bir plan yapmayı tercih ederim", "high": "right", "subscale": "Yapısal stil"},
    {"no": 10, "text": "Benim için sosyal ortamlarda rahat / esnek olmak…", "left": "Önemli değildir", "right": "Çok önemlidir", "high": "right", "subscale": "Sosyal yeterlilik"},
    {"no": 11, "text": "Ailemle birlikteyken kendimi… hissederim", "left": "Çok mutlu", "right": "Çok mutsuz", "high": "left", "subscale": "Aile uyumu"},
    {"no": 12, "text": "Beni…", "left": "Bazı yakın arkadaşlarım / aile üyelerim cesaretlendirebilir", "right": "Hiç kimse cesaretlendiremez", "high": "left", "subscale": "Sosyal kaynaklar"},
    {"no": 13, "text": "Yeteneklerim…", "left": "Olduğuna çok inanırım", "right": "Konusunda emin değilim", "high": "left", "subscale": "Kendilik algısı"},
    {"no": 14, "text": "Geleceğimin… olduğunu hissediyorum", "left": "Ümit verici", "right": "Belirsiz", "high": "left", "subscale": "Gelecek algısı"},
    {"no": 15, "text": "Şu konuda iyiyimdir…", "left": "Zamanımı planlama", "right": "Zamanımı harcama", "high": "left", "subscale": "Yapısal stil"},
    {"no": 16, "text": "Yeni arkadaşlık konusu… bir şeydir", "left": "Kolayca yapabildiğim", "right": "Yapmakta zorlandığım", "high": "left", "subscale": "Sosyal yeterlilik"},
    {"no": 17, "text": "Ailem şöyle tanımlanabilir…", "left": "Birbirinden bağımsız", "right": "Birbirine sıkı biçimde kenetlenmiş", "high": "right", "subscale": "Aile uyumu"},
    {"no": 18, "text": "Arkadaşlarımın arasındaki ilişkiler…", "left": "Zayıftır", "right": "Güçlüdür", "high": "right", "subscale": "Sosyal kaynaklar"},
    {"no": 19, "text": "Yargılarıma ve kararlarıma…", "left": "Çok fazla güvenmem", "right": "Tamamen güvenirim", "high": "right", "subscale": "Kendilik algısı"},
    {"no": 20, "text": "Geleceğe dönük amaçlarım…", "left": "Belirsizdir", "right": "İyi düşünülmüştür", "high": "right", "subscale": "Gelecek algısı"},
    {"no": 21, "text": "Kurallar ve düzenli alışkanlıklar…", "left": "Günlük yaşamımda yoktur", "right": "Günlük yaşamımı kolaylaştırır", "high": "right", "subscale": "Yapısal stil"},
    {"no": 22, "text": "Yeni insanlarla tanışmak…", "left": "Benim için zordur", "right": "Benim iyi olduğum bir konudur", "high": "right", "subscale": "Sosyal yeterlilik"},
    {"no": 23, "text": "Zor zamanlarda, ailem…", "left": "Geleceğe pozitif bakar", "right": "Geleceği umutsuz görür", "high": "left", "subscale": "Aile uyumu"},
    {"no": 24, "text": "Ailemden birisi acil bir durumla karşılaştığında…", "left": "Bana hemen haber verilir", "right": "Bana söylenmesi bir hayli zaman alır", "high": "left", "subscale": "Sosyal kaynaklar"},
    {"no": 25, "text": "Diğerleriyle beraberken…", "left": "Kolayca gülerim", "right": "Nadiren gülerim", "high": "left", "subscale": "Sosyal yeterlilik"},
    {"no": 26, "text": "Başka kişiler söz konusu olduğunda, ailem şöyle davranır:", "left": "Birbirlerini desteklemez biçimde", "right": "Birbirlerine bağlı biçimde", "high": "right", "subscale": "Aile uyumu"},
    {"no": 27, "text": "Destek alırım…", "left": "Arkadaşlarımdan / aile üyelerinden", "right": "Hiç kimseden", "high": "left", "subscale": "Sosyal kaynaklar"},
    {"no": 28, "text": "Zor zamanlarda… eğilimim vardır", "left": "Her şeyi umutsuzca gören biri olma", "right": "Beni başarıya götürebilecek iyi bir şey bulma", "high": "right", "subscale": "Kendilik algısı"},
    {"no": 29, "text": "Karşılıklı konuşma için güzel konuların düşünülmesi, benim için…", "left": "Zordur", "right": "Kolaydır", "high": "right", "subscale": "Sosyal yeterlilik"},
    {"no": 30, "text": "İhtiyacım olduğunda…", "left": "Bana yardım edebilecek kimse yoktur", "right": "Her zaman bana yardım edebilen birisi vardır", "high": "right", "subscale": "Sosyal kaynaklar"},
    {"no": 31, "text": "Hayatımdaki kontrol edemediğim olaylar ile…", "left": "Başa çıkmaya çalışırım", "right": "Sürekli bir endişe / kaygı kaynağıdır", "high": "left", "subscale": "Kendilik algısı"},
    {"no": 32, "text": "Ailemde şunu severiz…", "left": "İşleri bağımsız olarak yapmayı", "right": "İşleri hep beraber yapmayı", "high": "right", "subscale": "Aile uyumu"},
    {"no": 33, "text": "Yakın arkadaşlarım / aile üyeleri…", "left": "Yeteneklerimi beğenirler", "right": "Yeteneklerimi beğenmezler", "high": "left", "subscale": "Sosyal kaynaklar"},
]

SUBSCALE_ORDER = [
    "Kendilik algısı",
    "Gelecek algısı",
    "Yapısal stil",
    "Sosyal yeterlilik",
    "Aile uyumu",
    "Sosyal kaynaklar",
]


def score_item(raw_value: int, high_side: str) -> int:
    return raw_value if high_side == "right" else 6 - raw_value


def level_band(score: float) -> str:
    if score < 2.0:
        return "Düşük"
    if score < 2.75:
        return "Düşük-orta"
    if score < 3.50:
        return "Orta"
    if score < 4.25:
        return "İyi"
    return "Çok iyi"


def general_level_comment(score: float) -> str:
    if score < 2.0:
        return (
            "Genel profil düşük düzeyde görünmektedir. Bu durum, katılımcının zorlayıcı yaşam olayları karşısında "
            "kendi kaynaklarını fark etmekte, sosyal destek aramakta veya gelecek ve planlama alanlarında güçlük yaşayabileceğini düşündürür. "
            "Bu sonuç kişisel yetersizlik anlamına gelmez; desteklenebilir alanları görünür kılar."
        )
    if score < 2.75:
        return (
            "Genel profil düşük-orta düzeyde görünmektedir. Katılımcının bazı dayanıklılık kaynakları mevcut olmakla birlikte, "
            "bu kaynakların stres dönemlerinde düzenli ve etkili biçimde kullanılması zorlaşabilir. Küçük, somut ve sürdürülebilir destek adımları yararlı olabilir."
        )
    if score < 3.50:
        return (
            "Genel profil orta düzeydedir. Bu örüntü, katılımcının bazı psikolojik ve sosyal kaynaklara sahip olduğunu; "
            "ancak bu kaynakların bazı durumlarda dalgalanabileceğini veya daha bilinçli kullanılmaya ihtiyaç duyabileceğini gösterir."
        )
    if score < 4.25:
        return (
            "Genel profil iyi düzeydedir. Katılımcının zorlayıcı durumlarla baş etmesini kolaylaştırabilecek belirgin kaynakları vardır. "
            "Bu aşamada amaç, güçlü alanları korumak ve daha düşük kalan alanları hedefli biçimde güçlendirmektir."
        )
    return (
        "Genel profil çok iyi düzeydedir. Katılımcı, bireysel ve/veya sosyal kaynaklarını zorlayıcı durumlarda kullanabilecek güçlü bir dayanıklılık örüntüsü göstermektedir. "
        "Yüksek puan hiç zorlanmayacağı anlamına gelmez; toparlanmayı kolaylaştırabilecek kaynakların güçlü algılandığını gösterir."
    )


def generate_profile_commentary(subscale_scores: dict) -> dict:
    strongest = max(subscale_scores, key=subscale_scores.get)
    weakest = min(subscale_scores, key=subscale_scores.get)

    personal_domains = ["Kendilik algısı", "Gelecek algısı", "Yapısal stil"]
    relational_domains = ["Sosyal yeterlilik", "Aile uyumu", "Sosyal kaynaklar"]

    personal_mean = sum(subscale_scores[d] for d in personal_domains) / len(personal_domains)
    relational_mean = sum(subscale_scores[d] for d in relational_domains) / len(relational_domains)
    spread = max(subscale_scores.values()) - min(subscale_scores.values())

    if spread >= 1.50:
        distribution = (
            "Alt boyutlar arasında belirgin farklılaşma vardır. Bu, dayanıklılık kaynaklarının homojen dağılmadığını gösterir. "
            "Bazı alanlar güçlü bir dayanak oluştururken bazı alanlar zorlayıcı dönemlerde kırılganlık yaratabilir."
        )
    elif spread >= 0.80:
        distribution = (
            "Alt boyutlar arasında orta düzeyde farklılaşma vardır. Katılımcının dayanıklılık kaynakları genel olarak mevcut görünmekle birlikte, "
            f"{strongest} alanı daha güçlü bir kaynak, {weakest} alanı ise daha fazla desteklenebilecek alan olarak görünmektedir."
        )
    else:
        distribution = (
            "Alt boyutlar birbirine görece yakın görünmektedir. Bu, dayanıklılık kaynaklarının daha dengeli dağıldığını düşündürür. "
            "Bu durumda amaç tek bir alanı düzeltmekten çok, tüm kaynakları düzenli biçimde korumak ve güçlendirmektir."
        )

    if personal_mean >= relational_mean + 0.50:
        balance = (
            f"Kişisel/içsel kaynaklar ortalaması ({personal_mean:.2f}), sosyal/ilişkisel kaynaklar ortalamasından ({relational_mean:.2f}) daha yüksektir. "
            "Bu örüntü, katılımcının daha çok kendi problem çözme kapasitesi, planlama becerisi veya gelecek yönelimine yaslandığını düşündürür."
        )
    elif relational_mean >= personal_mean + 0.50:
        balance = (
            f"Sosyal/ilişkisel kaynaklar ortalaması ({relational_mean:.2f}), kişisel/içsel kaynaklar ortalamasından ({personal_mean:.2f}) daha yüksektir. "
            "Bu örüntü, katılımcının çevresel desteklerden güç aldığını; bireysel alanların ayrıca desteklenebileceğini düşündürür."
        )
    else:
        balance = (
            f"Kişisel/içsel kaynaklar ({personal_mean:.2f}) ile sosyal/ilişkisel kaynaklar ({relational_mean:.2f}) birbirine yakın düzeydedir. "
            "Bu, dayanıklılığın hem bireysel hem de sosyal kaynaklarla desteklendiğini gösteren dengeli bir örüntü olabilir."
        )

    return {
        "strongest": strongest,
        "weakest": weakest,
        "personal_mean": personal_mean,
        "relational_mean": relational_mean,
        "distribution": distribution,
        "balance": balance,
    }


def generate_personal_action_plan(subscale_scores: dict, total_mean: float) -> list:
    strongest = max(subscale_scores, key=subscale_scores.get)
    weakest = min(subscale_scores, key=subscale_scores.get)

    action_map = {
        "Kendilik algısı": [
            "Bu hafta daha önce başardığınız üç zor durumu yazın.",
            "Güncel bir problemi seçip bu problemi üç küçük çözüm adımına ayırın.",
            "Her günün sonunda 'Bugün baş edebildiğim bir şey neydi?' sorusuna kısa bir yanıt yazın."
        ],
        "Gelecek algısı": [
            "Bir haftalık küçük, gerçekçi ve ölçülebilir bir hedef belirleyin.",
            "Bu hedef için ilk 10 dakikalık adımı yazın.",
            "Hafta sonunda hedefin neden tamamlandığını ya da neden aksadığını yargılamadan değerlendirin."
        ],
        "Yapısal stil": [
            "Yarın için yalnızca üç öncelik yazın.",
            "Bir işi 15 dakikalık küçük bir parçaya bölerek başlatın.",
            "Uyku, yemek, çalışma veya hareket için bir sabit rutin seçip bir hafta uygulayın."
        ],
        "Sosyal yeterlilik": [
            "Güvende hissettiğiniz biriyle kısa bir iletişim başlatın.",
            "Bir sosyal ortamda en az bir açık uçlu soru sorun.",
            "Yardım istemeniz gerekse kullanacağınız bir cümleyi önceden yazın."
        ],
        "Aile uyumu": [
            "Aileden beklediğiniz bir desteği somut olarak yazın.",
            "Bu beklentiyi suçlayıcı olmayan bir 'ben dili' cümlesine dönüştürün.",
            "Aile içinde kısa ama olumlu bir ortak zaman planlayın."
        ],
        "Sosyal kaynaklar": [
            "Destek alabileceğiniz üç kişiyi listeleyin.",
            "Her kişinin hangi konuda destek olabileceğini yazın.",
            "Bu hafta bu kişilerden biriyle kısa bir temas kurun."
        ],
    }

    plan = []

    plan.append(
        f"En güçlü alan olan '{strongest}' alanını korumak için: "
        f"Bu alanın size hangi durumlarda yardımcı olduğunu fark edin ve zorlandığınızda bilinçli olarak kullanın."
    )

    for item in action_map[weakest]:
        plan.append(f"Öncelikli gelişim alanı olan '{weakest}' için: {item}")

    if total_mean < 2.75:
        plan.append(
            "Genel puan düşük-orta veya düşük aralıkta olduğu için hedefleri küçük tutun; "
            "aynı anda birçok değişiklik yapmaya çalışmayın."
        )

    plan.append(
        "Bir hafta sonra bu adımları gözden geçirin; işe yarayanları sürdürün, zor gelenleri daha küçük parçalara bölün."
    )

    return plan


def detailed_subscale_interpretation(subscale: str, score: float, strongest: str, weakest: str) -> str:
    info = {
        "Kendilik algısı": {
            "meaning": "Bu alt boyut, kişinin kendisini ne kadar yeterli, etkili ve baş edebilir gördüğünü değerlendirir. Problem çözme kapasitesine güvenme, beklenmedik olaylarda çözüm arayabilme, kararlarına güvenebilme ve kontrol edemediği durumlarda bile tamamen çaresiz hissetmeden işlevsel kalabilme ile ilişkilidir.",
            "low": "Kişi zorlayıcı olaylar karşısında kendi gücünü olduğundan daha sınırlı algılayabilir; karar vermeyi, girişimde bulunmayı ve yardım aramayı geciktirebilir.",
            "mid": "Kişi bazı durumlarda kendi becerilerine güvenebilir; ancak stres arttığında bu güven dalgalanabilir.",
            "high": "Kişi zorlayıcı olaylar karşısında kendi problem çözme kapasitesine daha kolay erişebilir ve kontrol edebildiği küçük alanlara odaklanabilir.",
            "daily": "Karar alma, kriz anında sakin kalabilme, problem karşısında seçenek üretebilme, hata yaptığında tamamen vazgeçmeme ve yeniden deneme kapasitesiyle kendini gösterir.",
            "questions": [
                "Zorlandığım bir durumda daha önce hangi becerimi kullanarak toparlandım?",
                "Bu sorunun kontrol edebileceğim küçük bir parçası var mı?",
                "Bugün bu konuda atabileceğim en küçük gerçekçi adım nedir?"
            ],
            "suggestions": [
                "Geçmişte üstesinden gelinen üç güçlüğü yazın.",
                "Büyük problemleri küçük, uygulanabilir adımlara bölün.",
                "Karar verirken yalnızca riskleri değil, elinizdeki kaynakları da yazın."
            ]
        },
        "Gelecek algısı": {
            "meaning": "Bu alt boyut, geleceğe ilişkin umut, yön, amaç ve planlanabilirlik algısını değerlendirir. Hedeflerin ulaşılabilir görülmesi ve yaşamda yön duygusu hissedebilme ile ilişkilidir.",
            "low": "Gelecek belirsiz, dağınık veya tehdit edici algılanabilir; hedefler uygulanabilir adımlara dönüşmekte zorlanabilir.",
            "mid": "Geleceğe ilişkin bazı hedefler vardır; ancak bunlar her zaman net, sürdürülebilir veya somut olmayabilir.",
            "high": "Kişi geleceği kısmen planlanabilir ve şekillendirilebilir bir süreç olarak görebilir; bu da motivasyonu destekleyebilir.",
            "daily": "Hedef belirleme, uzun vadeli düşünme, umudu koruma, plan yapma ve yaşanan güçlüğü geçici bir dönem olarak görebilme ile kendini gösterir.",
            "questions": [
                "Önümüzdeki bir hafta içinde benim için anlamlı olacak küçük bir hedef nedir?",
                "Bu hedefe ulaşmak için ilk somut adımım ne olabilir?",
                "Geleceğe ilişkin kaygımın içinde çözüm üretebileceğim bir bölüm var mı?"
            ],
            "suggestions": [
                "Hedefleri kısa, orta ve uzun vadeli olarak ayırın.",
                "Her hedef için tek bir ilk adım belirleyin.",
                "Haftalık küçük ilerlemeleri görünür hale getirin."
            ]
        },
        "Yapısal stil": {
            "meaning": "Bu alt boyut, zamanı kullanma, planlama, rutin oluşturma ve günlük yaşamı organize etme becerisini değerlendirir.",
            "low": "Kişi ne yapması gerektiğini bilse bile bunu plana dönüştürmekte zorlanabilir; erteleme, dağınıklık ve öncelik belirleme güçlüğü yaşayabilir.",
            "mid": "Planlama kısmen vardır; ancak yoğunluk, stres veya belirsizlik arttığında rutinler kolay aksayabilir.",
            "high": "Kişi plan, rutin ve önceliklendirmeden etkin biçimde yararlanabilir; bu da kontrol duygusunu destekler.",
            "daily": "Ajanda kullanma, işleri sıraya koyma, zamanı bölme, görevleri tamamlama ve zor dönemlerde temel rutini sürdürebilme ile kendini gösterir.",
            "questions": [
                "Bugün tamamlamam gereken en önemli üç iş nedir?",
                "Bu işlerden hangisi en küçük adımla başlayabilir?",
                "Rutinim bozulduğunda geri dönmemi kolaylaştıracak sabit bir alışkanlık ne olabilir?"
            ],
            "suggestions": [
                "Günlük üç öncelik belirleyin.",
                "Görevleri 15-20 dakikalık küçük parçalara bölün.",
                "Uyku, yemek, hareket ve çalışma için temel bir günlük iskelet oluşturun."
            ]
        },
        "Sosyal yeterlilik": {
            "meaning": "Bu alt boyut, sosyal ortamlarda rahatlık, iletişim başlatma ve sürdürme, yeni ilişkiler kurabilme ve sosyal etkileşimlerden güç alabilme kapasitesini değerlendirir.",
            "low": "Kişi sosyal ortamlarda çekingenlik, geri çekilme veya iletişim başlatmada zorlanma yaşayabilir; bu durum destek alma kanallarını daraltabilir.",
            "mid": "Kişi bazı sosyal ortamlarda rahat olabilirken, bazı ortamlarda kendini gergin veya yetersiz hissedebilir.",
            "high": "Kişi sosyal etkileşimleri psikolojik dayanıklılığı destekleyen bir kaynak olarak kullanabilir.",
            "daily": "Konuşma başlatma, ihtiyaçlarını ifade etme, destek isteme, sosyal ortama katılma ve ilişkileri sürdürebilme ile kendini gösterir.",
            "questions": [
                "Kendimi daha güvende hissettiğim sosyal ortamlar hangileri?",
                "Bugün başlatabileceğim küçük bir sosyal temas ne olabilir?",
                "Yardım istemem gerekse bunu kime ve nasıl söyleyebilirim?"
            ],
            "suggestions": [
                "Küçük ve güvenli sosyal temaslarla başlayın.",
                "Sohbet başlatmak için birkaç basit konu belirleyin.",
                "Aktif dinleme ve açık uçlu soru sorma becerilerini kullanın."
            ]
        },
        "Aile uyumu": {
            "meaning": "Bu alt boyut, aile içinde duygusal yakınlık, ortak anlayış, bağlılık, desteklenme ve kriz dönemlerinde birlikte hareket edebilme algısını değerlendirir.",
            "low": "Kişi aile içinde yeterince anlaşılmadığını, desteklenmediğini veya zor zamanlarda yalnız kaldığını hissedebilir.",
            "mid": "Aile desteği kısmen mevcuttur; ancak her durumda tutarlı veya erişilebilir hissedilmeyebilir.",
            "high": "Aile, zorlayıcı dönemlerde güven veren, destekleyici ve toparlanmayı kolaylaştıran bir kaynak olarak işlev görebilir.",
            "daily": "Aileyle açık konuşabilme, zor zamanda yanında birilerinin olduğunu hissetme ve duygusal destek görebilme ile kendini gösterir.",
            "questions": [
                "Ailemden en çok hangi konuda destek bekliyorum?",
                "Bu desteği suçlayıcı olmayan bir dille nasıl ifade edebilirim?",
                "Aile içinde iyi gelen temas veya ortak zaman biçimleri neler?"
            ],
            "suggestions": [
                "Destek beklentilerinizi somut cümlelerle ifade edin.",
                "Aile içinde 'ben dili' kullanın.",
                "Kısa ama düzenli ortak zamanlar planlayın."
            ]
        },
        "Sosyal kaynaklar": {
            "meaning": "Bu alt boyut, arkadaşlar, aile üyeleri veya yakın çevreden algılanan destek kaynaklarını değerlendirir. Yardım isteyebilme ve yalnız olmadığını hissetme ile ilişkilidir.",
            "low": "Kişi sorunları tek başına taşımaya eğilimli olabilir; yardım istemek zor veya yük olmak gibi algılanabilir.",
            "mid": "Destek kaynakları vardır; ancak kişi bu kaynaklara her zaman kolay ulaşamayabilir.",
            "high": "Kişi zorlayıcı dönemlerde duygusal, pratik veya bilgilendirici destek alabileceği kişilere daha kolay ulaşabilir.",
            "daily": "Güvenilir kişilere ulaşabilme, yardım isteme, destekleyici ilişkileri sürdürme ve kriz anında yalnız hissetmeme ile kendini gösterir.",
            "questions": [
                "Zorlandığımda arayabileceğim üç kişi kim?",
                "Bu kişilerden hangi konuda destek isteyebilirim?",
                "Destek istemeyi kolaylaştıracak ilk cümlem ne olabilir?"
            ],
            "suggestions": [
                "Destek haritası oluşturun.",
                "Yardım isteme cümlelerini önceden hazırlayın.",
                "Sosyal ilişkileri kriz dışı zamanlarda da sürdürün."
            ]
        },
    }

    d = info[subscale]

    if score < 2.75:
        level_text = d["low"]
    elif score < 3.50:
        level_text = d["mid"]
    else:
        level_text = d["high"]

    profile_note = ""
    if subscale == strongest:
        profile_note = " Profil içindeki yeri: Bu alan katılımcının en güçlü görünen kaynağıdır; diğer gelişim alanlarını desteklemek için kullanılabilir."
    elif subscale == weakest:
        profile_note = " Profil içindeki yeri: Bu alan katılımcının en fazla desteklenebilecek alanıdır; küçük ve somut hedeflerle güçlendirilebilir."

    questions = "\n".join([f"- {q}" for q in d["questions"]])
    suggestions = "\n".join([f"- {s}" for s in d["suggestions"]])

    return (
        f"{d['meaning']}\n\n"
        f"Puan yorumu: {score:.2f}/5; betimleyici düzey: {level_band(score)}. {level_text}{profile_note}\n\n"
        f"Günlük yaşamdaki karşılığı: {d['daily']}\n\n"
        f"Katılımcının kendisine sorabileceği sorular:\n{questions}\n\n"
        f"Bu alanı güçlendirmek için öneriler:\n{suggestions}"
    )


def build_report(participant_name, participant_code, age, gender, subscale_scores, total_mean):
    commentary = generate_profile_commentary(subscale_scores)
    strongest = commentary["strongest"]
    weakest = commentary["weakest"]

    lines = []
    lines.append("YETİŞKİNLER İÇİN PSİKOLOJİK DAYANIKLILIK ÖLÇEĞİ")
    lines.append("YORUMLU BİREYSEL ANALİZ RAPORU")
    lines.append("")
    lines.append("Katılımcı Bilgileri")
    lines.append(f"Katılımcı: {participant_name if participant_name else 'Belirtilmedi'}")
    lines.append(f"Katılımcı kodu: {participant_code if participant_code else 'Belirtilmedi'}")
    lines.append(f"Yaş: {age if age else 'Belirtilmedi'}")
    lines.append(f"Cinsiyet: {gender if gender else 'Belirtilmedi'}")
    lines.append(f"Rapor tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    lines.append("")
    lines.append("1. Genel Psikolojik Dayanıklılık Yorumu")
    lines.append(f"Genel ortalama: {total_mean:.2f}/5 | Düzey: {level_band(total_mean)}")
    lines.append(general_level_comment(total_mean))
    lines.append("")
    lines.append("2. Profil Dağılımının Yorumu")
    lines.append(commentary["distribution"])
    lines.append("")
    lines.append("3. Kişisel ve Sosyal Kaynak Dengesi")
    lines.append(commentary["balance"])
    lines.append("")
    lines.append("4. Güçlü Alan ve Gelişim Alanı")
    lines.append(f"En güçlü alan: {strongest} ({subscale_scores[strongest]:.2f}/5)")
    lines.append(f"En fazla desteklenebilecek alan: {weakest} ({subscale_scores[weakest]:.2f}/5)")
    lines.append("")
    lines.append("5. KATILIMCIYA ÖZEL MİNİ EYLEM PLANI")
    lines.append("Bu bölüm, katılımcının puan örüntüsüne göre otomatik oluşturulmuştur.")
    for i, action in enumerate(generate_personal_action_plan(subscale_scores, total_mean), start=1):
        lines.append(f"{i}) {action}")
    lines.append("")
    lines.append("6. Alt Boyutlara Göre Ayrıntılı Yorumlar")
    for sub, score in subscale_scores.items():
        lines.append("")
        lines.append(f"{sub} — {score:.2f}/5")
        lines.append(detailed_subscale_interpretation(sub, score, strongest, weakest))
    lines.append("")
    lines.append("7. Önemli Not")
    lines.append("Bu rapor tanı koymaz ve klinik değerlendirme yerine geçmez. Sonuçlar yalnızca ölçek yanıtlarına dayalı betimleyici ve psiko-eğitimsel geri bildirimdir.")
    return "\n".join(lines)


st.title("🧭 Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği")
st.caption("Katılımcı ölçeği bireysel olarak doldurur; uygulama sonunda kişiye özel yorumlu analiz raporu üretir.")

with st.expander("Uygulama hakkında kısa bilgi", expanded=True):
    st.write(
        "Bu uygulama, 33 maddelik Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği yanıtlarını altı alt boyutta özetler: "
        "kendilik algısı, gelecek algısı, yapısal stil, sosyal yeterlilik, aile uyumu ve sosyal kaynaklar. "
        "Yüksek puanlar ilgili alanda daha güçlü psikolojik dayanıklılık kaynaklarına işaret eder."
    )
    st.warning(
        "Bu uygulama tanı koymaz ve klinik değerlendirme yerine geçmez. Rapor yalnızca bilgilendirme ve öz değerlendirme amacıyla hazırlanır."
    )

st.subheader("Katılımcı Bilgileri")

col1, col2 = st.columns(2)

with col1:
    participant_name = st.text_input("Ad Soyad / Rumuz", "")
    age = st.number_input("Yaş", min_value=18, max_value=100, value=25, step=1)

with col2:
    participant_code = st.text_input("Katılımcı kodu", "")
    gender = st.selectbox("Cinsiyet", ["Belirtmek istemiyorum", "Kadın", "Erkek", "Diğer"])

st.divider()

st.subheader("Ölçek Maddeleri")

st.markdown(
    """
    <div class="scale-help">
    Her madde için kendinize en yakın kutucuğu seçiniz. <strong>1 sol uca</strong>, <strong>5 sağ uca</strong> en yakın yanıtı ifade eder.
    Orta değer olan <strong>3</strong>, iki ifade arasında daha dengeli/kararsız bir konumu gösterir.
    </div>
    """,
    unsafe_allow_html=True
)

responses = {}

for item in ITEMS:
    st.markdown(
        f"""
        <div class="question-box">
            <div class="question-title">{item['no']}. {item['text']}</div>
            <div class="anchor-text"><strong>1 - Sol uç:</strong> {item['left']}</div>
            <div class="anchor-text"><strong>5 - Sağ uç:</strong> {item['right']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    responses[item["no"]] = st.radio(
        label="Seçiminiz",
        options=[1, 2, 3, 4, 5],
        index=2,
        horizontal=True,
        key=f"item_{item['no']}",
        label_visibility="collapsed"
    )

    st.write("")

submitted = st.button("Raporu Oluştur", type="primary")

if submitted:
    scored_rows = []

    for item in ITEMS:
        raw = responses[item["no"]]
        scored = score_item(raw, item["high"])

        scored_rows.append({
            "Madde": item["no"],
            "Alt boyut": item["subscale"],
            "Ham yanıt": raw,
            "Dayanıklılık yönünde puan": scored
        })

    df = pd.DataFrame(scored_rows)

    subscale_scores_raw = df.groupby("Alt boyut")["Dayanıklılık yönünde puan"].mean().to_dict()
    subscale_scores = {k: subscale_scores_raw[k] for k in SUBSCALE_ORDER}
    total_mean = df["Dayanıklılık yönünde puan"].mean()

    commentary = generate_profile_commentary(subscale_scores)
    strongest = commentary["strongest"]
    weakest = commentary["weakest"]

    st.success("Rapor oluşturuldu.")

    st.subheader("Genel Sonuç")
    st.metric("Genel psikolojik dayanıklılık ortalaması", f"{total_mean:.2f} / 5")
    st.write(f"**Betimleyici düzey:** {level_band(total_mean)}")
    st.write(general_level_comment(total_mean))

    st.markdown("## 📝 Katılımcıya Özel Mini Eylem Planı")

    st.info(
        "Bu bölüm, katılımcının puan örüntüsüne göre otomatik oluşturulur. "
        "En güçlü alan korunurken, en fazla desteklenebilecek alan için küçük ve uygulanabilir adımlar önerilir."
    )

    action_plan = generate_personal_action_plan(subscale_scores, total_mean)

    plan_html = """
    <div class='report-box'>
    """

    for idx, action in enumerate(action_plan, start=1):
        plan_html += f"<p><strong>{idx}.</strong> {action}</p>"

    plan_html += "</div>"

    st.markdown(plan_html, unsafe_allow_html=True)

    st.subheader("Alt Boyut Puanları")

    result_df = pd.DataFrame({
        "Alt boyut": list(subscale_scores.keys()),
        "Ortalama puan": [round(v, 2) for v in subscale_scores.values()],
        "Betimleyici düzey": [level_band(v) for v in subscale_scores.values()]
    })

    st.dataframe(result_df, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(result_df["Alt boyut"], result_df["Ortalama puan"])
    ax.set_ylim(0, 5)
    ax.set_ylabel("Ortalama puan")
    ax.set_title("Alt Boyutlara Göre Psikolojik Dayanıklılık Profili")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

    st.subheader("Kişiye Özel Yorumlu Analiz")

    st.markdown("### Profil dağılımı")
    st.markdown(
        f"<div class='report-box'>{commentary['distribution']}</div>",
        unsafe_allow_html=True
    )

    st.markdown("### Kişisel kaynaklar ve sosyal kaynaklar dengesi")
    st.markdown(
        f"""
        <div class="report-box">
        <strong>Kişisel/içsel kaynaklar ortalaması:</strong> {commentary["personal_mean"]:.2f}/5<br>
        <strong>Sosyal/ilişkisel kaynaklar ortalaması:</strong> {commentary["relational_mean"]:.2f}/5<br><br>
        {commentary["balance"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Güçlü alan ve gelişim alanı")
    st.markdown(
        f"""
        <div class="report-box">
        <strong>En güçlü görünen alan:</strong> {strongest} ({subscale_scores[strongest]:.2f}/5)<br>
        <strong>En fazla desteklenebilecek alan:</strong> {weakest} ({subscale_scores[weakest]:.2f}/5)
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🔎 Alt Boyutlara Göre Ayrıntılı Yorumlar")

    st.write(
        "Her alt boyut; anlamı, puan yorumu, günlük yaşamdaki karşılığı, "
        "katılımcının kendisine sorabileceği sorular ve güçlendirme önerileriyle birlikte verilmiştir."
    )

    for sub, score in subscale_scores.items():
        with st.expander(
            f"{sub}: {score:.2f}/5 — {level_band(score)}",
            expanded=(sub == strongest or sub == weakest)
        ):
            st.write(detailed_subscale_interpretation(sub, score, strongest, weakest))

    report_text = build_report(
        participant_name=participant_name,
        participant_code=participant_code,
        age=age,
        gender=gender,
        subscale_scores=subscale_scores,
        total_mean=total_mean
    )

    st.subheader("Bireysel Rapor")
    st.text_area("Rapor metni", report_text, height=520)

    csv_buffer = io.StringIO()

    export_df = df.copy()
    export_df.insert(0, "Katılımcı", participant_name)
    export_df.insert(1, "Katılımcı kodu", participant_code)
    export_df.insert(2, "Tarih", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    export_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")

    st.download_button(
        "Raporu TXT olarak indir",
        data=report_text.encode("utf-8"),
        file_name=f"psikolojik_dayaniklilik_raporu_{participant_code or 'katilimci'}.txt",
        mime="text/plain"
    )

    st.download_button(
        "Madde puanlarını CSV olarak indir",
        data=csv_buffer.getvalue().encode("utf-8-sig"),
        file_name=f"psikolojik_dayaniklilik_puanlari_{participant_code or 'katilimci'}.csv",
        mime="text/csv"
    )
