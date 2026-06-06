
import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği",
    page_icon="🧭",
    layout="centered"
)

# ------------------------------------------------------------
# Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği
# Kaynak yapısı:
# - 33 madde
# - 6 alt boyut:
#   Kendilik algısı: 1, 7, 13, 19, 28, 31
#   Gelecek algısı: 2, 8, 14, 20
#   Yapısal stil: 3, 9, 15, 21
#   Sosyal yeterlilik: 4, 10, 16, 22, 25, 29
#   Aile uyumu: 5, 11, 17, 23, 26, 32
#   Sosyal kaynaklar: 6, 12, 18, 24, 27, 30, 33
#
# Puanlama:
# Her madde 1-5 arası yanıtlanır. Olumlu/dayanıklılığı temsil eden uç
# bazı maddelerde solda, bazı maddelerde sağdadır.
# Bu nedenle her madde dayanıklılık yönünde yeniden puanlanır.
# Yüksek puan daha yüksek psikolojik dayanıklılık göstergesi olarak yorumlanır.
#
# Not:
# Bu uygulama tanı koymaz; yalnızca ölçek yanıtlarına dayalı betimleyici
# bir bireysel geri bildirim raporu üretir.
# ------------------------------------------------------------

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

SUBSCALE_INFO = {
    "Kendilik algısı": "Kişinin problem çözme, kendi yeteneklerine güvenme ve zorlayıcı durumlarla baş etme algısını yansıtır.",
    "Gelecek algısı": "Geleceğe ilişkin umut, amaç ve planların ulaşılabilirliğine dair algıyı yansıtır.",
    "Yapısal stil": "Planlama, düzen, hedef belirleme ve günlük yaşamı yapılandırma eğilimini yansıtır.",
    "Sosyal yeterlilik": "Sosyal ortamlarda rahatlık, yeni ilişkiler kurabilme ve iletişim becerisine dair algıyı yansıtır.",
    "Aile uyumu": "Aile içi bağlılık, ortak anlayış, destek ve zor zamanlarda birlikte durabilme algısını yansıtır.",
    "Sosyal kaynaklar": "Arkadaşlar ve aile üyeleri gibi yakın çevreden algılanan destek kaynaklarını yansıtır.",
}

def score_item(raw_value: int, high_side: str) -> int:
    """Slider value: 1=left anchor, 5=right anchor. Output: 1-5 in resilience direction."""
    return raw_value if high_side == "right" else 6 - raw_value

def interpret_mean(x: float):
    # Descriptive bands only; not clinical/normative cutoffs.
    if x < 2.5:
        return "Geliştirilmeye açık alan", "Bu boyutta dayanıklılığı destekleyen kaynakların görece sınırlı algılandığı görülmektedir."
    elif x < 3.5:
        return "Orta düzey / dengeli alan", "Bu boyutta bazı koruyucu kaynaklar mevcut görünmekle birlikte güçlendirilebilir."
    else:
        return "Güçlü alan", "Bu boyutta dayanıklılığı destekleyen kaynakların belirgin olduğu görülmektedir."

def build_report(participant_name, participant_code, age, gender, subscale_scores, total_mean):
    strongest = max(subscale_scores, key=subscale_scores.get)
    weakest = min(subscale_scores, key=subscale_scores.get)
    total_label, total_comment = interpret_mean(total_mean)

    lines = []
    lines.append("YETİŞKİNLER İÇİN PSİKOLOJİK DAYANIKLILIK ÖLÇEĞİ")
    lines.append("Bireysel Geri Bildirim Raporu")
    lines.append("")
    lines.append(f"Katılımcı: {participant_name if participant_name else 'Belirtilmedi'}")
    lines.append(f"Katılımcı kodu: {participant_code if participant_code else 'Belirtilmedi'}")
    lines.append(f"Yaş: {age if age else 'Belirtilmedi'}")
    lines.append(f"Cinsiyet: {gender if gender else 'Belirtilmedi'}")
    lines.append(f"Rapor tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    lines.append("")
    lines.append("Genel sonuç")
    lines.append(f"Genel psikolojik dayanıklılık ortalaması: {total_mean:.2f} / 5")
    lines.append(f"Genel betimleyici düzey: {total_label}")
    lines.append(total_comment)
    lines.append("")
    lines.append("Alt boyut sonuçları")
    for sub, score in subscale_scores.items():
        label, comment = interpret_mean(score)
        lines.append(f"- {sub}: {score:.2f} / 5 | {label}")
        lines.append(f"  {SUBSCALE_INFO[sub]} {comment}")
    lines.append("")
    lines.append(f"En güçlü görünen alan: {strongest} ({subscale_scores[strongest]:.2f}/5)")
    lines.append(f"Geliştirilmeye en açık görünen alan: {weakest} ({subscale_scores[weakest]:.2f}/5)")
    lines.append("")
    lines.append("Yorum notu")
    lines.append("Bu rapor klinik tanı veya psikiyatrik değerlendirme yerine geçmez. Sonuçlar yalnızca kişinin ölçek maddelerine verdiği yanıtlara dayalı betimleyici bir geri bildirimdir.")
    lines.append("Düşük görünen alanlar kişisel zayıflık olarak değil, desteklenebilecek psikolojik ve sosyal kaynak alanları olarak değerlendirilmelidir.")
    return "\n".join(lines)

st.title("🧭 Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği")
st.caption("Katılımcı ölçeği bireysel olarak doldurur; uygulama sonunda kişiye özel betimleyici analiz raporu üretir.")

with st.expander("Uygulama hakkında kısa bilgi", expanded=True):
    st.write(
        "Bu uygulama, 33 maddelik Yetişkinler İçin Psikolojik Dayanıklılık Ölçeği yanıtlarını "
        "altı alt boyutta özetler: kendilik algısı, gelecek algısı, yapısal stil, sosyal yeterlilik, "
        "aile uyumu ve sosyal kaynaklar. Yüksek puanlar ilgili alanda daha güçlü psikolojik dayanıklılık "
        "kaynaklarına işaret eder."
    )
    st.warning(
        "Bu uygulama tanı koymaz ve klinik değerlendirme yerine geçmez. Rapor yalnızca bilgilendirme ve "
        "öz değerlendirme amacıyla hazırlanır."
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
st.write("Her madde için kendinize en yakın kutucuğu seçiniz. Sol uç 1, sağ uç 5 olarak düşünülmelidir.")

responses = {}

for item in ITEMS:
    st.markdown(f"**{item['no']}. {item['text']}**")
    st.caption(f"Sol uç: {item['left']}  |  Sağ uç: {item['right']}")
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
    subscale_scores = df.groupby("Alt boyut")["Dayanıklılık yönünde puan"].mean().to_dict()
    # Stable order
    subscale_order = ["Kendilik algısı", "Gelecek algısı", "Yapısal stil", "Sosyal yeterlilik", "Aile uyumu", "Sosyal kaynaklar"]
    subscale_scores = {k: subscale_scores[k] for k in subscale_order}
    total_mean = df["Dayanıklılık yönünde puan"].mean()

    st.success("Rapor oluşturuldu.")

    st.subheader("Genel Sonuç")
    total_label, total_comment = interpret_mean(total_mean)
    st.metric("Genel psikolojik dayanıklılık ortalaması", f"{total_mean:.2f} / 5")
    st.write(f"**Betimleyici düzey:** {total_label}")
    st.write(total_comment)

    st.subheader("Alt Boyut Puanları")
    result_df = pd.DataFrame({
        "Alt boyut": list(subscale_scores.keys()),
        "Ortalama puan": [round(v, 2) for v in subscale_scores.values()],
        "Betimleyici düzey": [interpret_mean(v)[0] for v in subscale_scores.values()]
    })
    st.dataframe(result_df, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(result_df["Alt boyut"], result_df["Ortalama puan"])
    ax.set_ylim(0, 5)
    ax.set_ylabel("Ortalama puan")
    ax.set_title("Alt Boyutlara Göre Psikolojik Dayanıklılık Profili")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

    st.subheader("Kişiye Özel Yorum")
    strongest = max(subscale_scores, key=subscale_scores.get)
    weakest = min(subscale_scores, key=subscale_scores.get)
    st.write(f"**En güçlü görünen alan:** {strongest} ({subscale_scores[strongest]:.2f}/5)")
    st.write(f"**Geliştirilmeye en açık görünen alan:** {weakest} ({subscale_scores[weakest]:.2f}/5)")

    for sub, score in subscale_scores.items():
        label, comment = interpret_mean(score)
        with st.expander(f"{sub}: {score:.2f}/5 — {label}"):
            st.write(SUBSCALE_INFO[sub])
            st.write(comment)

    report_text = build_report(
        participant_name=participant_name,
        participant_code=participant_code,
        age=age,
        gender=gender,
        subscale_scores=subscale_scores,
        total_mean=total_mean
    )

    st.subheader("Bireysel Rapor")
    st.text_area("Rapor metni", report_text, height=420)

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

    st.info(
        "Araştırma amaçlı toplu veri tutmak isterseniz CSV dosyalarını birleştirebiliriz ya da uygulamaya "
        "otomatik toplu kayıt özelliği ekleyebiliriz."
    )
