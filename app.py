import streamlit as st
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği",
    page_icon="🧭",
    layout="centered"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 17px !important;
}
.main .block-container {
    max-width: 1000px;
    padding-top: 1.5rem;
}
h1 {
    font-size: 2.15rem !important;
}
h2, h3 {
    font-size: 1.45rem !important;
}
p, li, div, span, label {
    font-size: 1rem !important;
    line-height: 1.45 !important;
}
.stCaptionContainer, .stCaptionContainer p {
    font-size: 0.95rem !important;
}
.stRadio label, .stRadio div, .stRadio span, .stRadio p {
    font-size: 1.05rem !important;
}
div[role="radiogroup"] label p {
    font-size: 1.08rem !important;
    font-weight: 600 !important;
}
.stButton button, .stDownloadButton button {
    font-size: 1rem !important;
    padding: 0.55rem 0.9rem !important;
}
.question-box {
    background-color:#f7f7f9;
    border:1px solid #e2e2e8;
    border-radius:14px;
    padding:16px 18px;
    margin-top:10px;
    margin-bottom:10px;
}
.question-title {
    font-size:1.12rem !important;
    font-weight:700;
    margin-bottom:8px;
}
.anchor-text {
    font-size:1rem !important;
    color:#333;
    margin-bottom:5px;
}
.scale-help {
    font-size:0.95rem !important;
    color:#555;
    margin-top:8px;
}
.report-box {
    background-color:#fbfbfd;
    border-left:5px solid #b8b8c8;
    padding:16px 18px;
    border-radius:10px;
    margin:12px 0 18px 0;
}
.report-box p, .report-box div, .report-box strong {
    font-size:1rem !important;
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
    return (
        f"Bu alt boyut için puan {score:.2f}/5 olup betimleyici düzey {level_band(score)} olarak değerlendirilmiştir. "
        f"Bu alan, katılımcının psikolojik dayanıklılık profilindeki önemli kaynaklardan biridir. "
        f"Eğer bu alan güçlü görünüyorsa korunması, daha düşük görünüyorsa küçük ve uygulanabilir adımlarla desteklenmesi önerilir."
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
        "Bu uygulama, 33 maddelik Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği yanıtlarını altı alt boyutta özetler."
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
        "Her alt boyut; anlamı, puan yorumu ve güçlendirme önerileriyle birlikte verilmiştir."
    )

    for sub, score in subscale_scores.items():
        with st.expander(
            f"{sub}: {score:.2f}/5 — {level_band(score)}",
            expanded=(sub == strongest or sub == weakest)
        ):
            st.write(detailed_subscale_interpretation(sub, score, strongest, weakest))

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
