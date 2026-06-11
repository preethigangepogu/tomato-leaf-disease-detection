import gradio as gr
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load trained model
tomato_model = tf.keras.models.load_model("tomato_disease_model.h5")

# Define class labels for tomato diseases
class_labels = ['Bacterial Spot', 'Early Blight', 'Healthy', 'Late Blight', 'Septoria Leaf Spot', 'Yellow Leaf Curl Virus']

# Define translations for diseases, remedies, and pesticides
translations = {
    "English": {
        'Bacterial Spot': ('Bacterial Spot',
            'Remove affected leaves and avoid overhead watering. Apply copper-based fungicide weekly during infection. Improve air circulation by proper plant spacing.',
            'Mancozeb (Low), Copper Hydroxide (Medium), Streptomycin (High)'),
        'Early Blight': ('Early Blight',
            'Prune infected leaves and dispose of plant debris. Use organic compost tea as a preventive measure. Apply a fungicide like copper oxychloride if severe.',
            'Chlorothalonil (Low), Copper Oxychloride (Medium), Azoxystrobin (High)'),
        'Healthy': ('Healthy',
            'Your plant is healthy and needs no treatment. Maintain good watering and sunlight exposure. Regularly check for early disease symptoms.',
            'No pesticide needed'),
        'Late Blight': ('Late Blight',
            'Increase air circulation and avoid excessive moisture. Use a baking soda spray (1 tsp per liter of water). Remove and destroy affected plant parts immediately.',
            'Copper Sulfate (Low), Dimethomorph (Medium), Mancozeb (High)'),
        'Septoria Leaf Spot': ('Septoria Leaf Spot',
            'Avoid overhead watering to keep leaves dry. Use a garlic or neem oil spray weekly. Apply a fungicide like thiophanate-methyl if necessary.',
            'Chlorothalonil (Low), Thiophanate-methyl (Medium), Difenoconazole (High)'),
        'Yellow Leaf Curl Virus': ('Yellow Leaf Curl Virus',
            'Plant resistant varieties and use row covers early. Remove infected plants to prevent spreading. Control whiteflies, the main virus carriers.',
            'No chemical treatment available')
    },
    "Hindi": {
        'Bacterial Spot': ('जीवाणु धब्बा',
            'संक्रमित पत्तियों को हटाएं और ऊपर से पानी न डालें। तांबा-आधारित कवकनाशी साप्ताहिक रूप से लगाएं। पौधों के बीच उचित दूरी बनाए रखें।',
            'मैंकोज़ेब (कम), कॉपर हाइड्रॉक्साइड (मध्यम), स्ट्रेप्टोमाइसिन (उच्च)'),
        'Early Blight': ('प्रारंभिक झुलसा',
            'संक्रमित पत्तियों को हटा दें और कचरा नष्ट करें। जैविक कंपोस्ट चाय का उपयोग करें। गंभीर मामलों में कॉपर ऑक्सीक्लोराइड कवकनाशी लगाएं।',
            'क्लोरोथालोनिल (कम), कॉपर ऑक्सीक्लोराइड (मध्यम), एजोक्सीस्ट्रोबिन (उच्च)'),
        'Healthy': ('स्वस्थ',
            'आपका पौधा स्वस्थ है और उपचार की आवश्यकता नहीं। अच्छी पानी व्यवस्था और धूप सुनिश्चित करें। प्रारंभिक लक्षणों की नियमित जांच करें।',
            'कोई कीटनाशक आवश्यक नहीं'),
        'Late Blight': ('लेट ब्लाइट',
            'हवा का संचार बढ़ाएं और अधिक नमी से बचें। 1 लीटर पानी में 1 चम्मच बेकिंग सोडा मिलाकर स्प्रे करें। संक्रमित पौधों के भाग तुरंत नष्ट करें।',
            'कॉपर सल्फेट (कम), डाइमेथोमॉर्फ (मध्यम), मैंकोज़ेब (उच्च)'),
        'Septoria Leaf Spot': ('सेप्टोरिया लीफ स्पॉट',
            'ऊपर से पानी देने से बचें ताकि पत्तियाँ सूखी रहें। साप्ताहिक रूप से लहसुन या नीम तेल का छिड़काव करें। गंभीर मामलों में थायोफेनेट-मिथाइल कवकनाशी लगाएं।',
            'क्लोरोथालोनिल (कम), थायोफेनेट-मिथाइल (मध्यम), डाइफेनोकोनाज़ोल (उच्च)'),
        'Yellow Leaf Curl Virus': ('पीला पत्ता कर्ल वायरस',
            'रोग प्रतिरोधी किस्में लगाएं और शुरुआत में ही सुरक्षा उपाय अपनाएं। संक्रमित पौधों को तुरंत हटा दें। सफेद मक्खियों पर नियंत्रण रखें।',
            'कोई रासायनिक उपचार उपलब्ध नहीं')
    },
    "Telugu": {
        'Bacterial Spot': ('బాక్టీరియల్ స్పాట్',
            'పట్టుబడిన ఆకులను తొలగించండి మరియు పైనుంచి నీరు పోయకుండా ఉండండి. రాగి-ఆధారిత ఫంగిసైడ్‌ను వారానికి ఒకసారి ప్రయోగించండి.',
            'మాంకోజెబ్ (తక్కువ), కాపర్ హైడ్రాక్సైడ్ (మధ్యస్థ), స్ట్రెప్టోమైసిన్ (అధిక)'),
        'Early Blight': ('అకాల తెగులు',
            'సంబంధిత ఆకులను తీసివేయండి మరియు ఆకు చెత్తను తొలగించండి. సేంద్రీయ కంపోస్టు టీను నిరోధక చర్యగా ఉపయోగించండి. తీవ్రమైన దశలో కాపర్ ఆక్సీక్లోరైడ్ ఫంగిసైడ్‌ను ఉపయోగించండి.',
            'క్లోరోథాలోనిల్ (తక్కువ), కాపర్ ఆక్సీక్లోరైడ్ (మధ్యస్థ), అజోక్సీస్ట్రోబిన్ (అధిక)'),
        'Healthy': ('ఆరోగ్యకరమైనది',
            'మీ మొక్క ఆరోగ్యంగా ఉంది, చికిత్స అవసరం లేదు. మంచి నీరు మరియు సూర్యకాంతిని నిలిపివేయండి. మొదటి లక్షణాలను గమనించండి.',
            'పెస్టిసైడ్ అవసరం లేదు'),
        'Late Blight': ('లేట్ బ్లైట్',
            'గాలి ప్రసరణను పెంచండి మరియు తేమ తగ్గించండి. 1 లీటర్ నీటికి 1 టీస్పూన్ బేకింగ్ సోడా కలిపి స్ప్రే చేయండి.',
            'కాపర్ సల్ఫేట్ (తక్కువ), డైమెథోమార్ఫ్ (మధ్యస్థ), మాంకోజెబ్ (అధిక)'),
        'Septoria Leaf Spot': ('సెప్టోరియా లీఫ్ స్పాట్',
            'మొక్కల పై నీటిని పోయకుండా ఉండండి. వారానికి ఒకసారి వెల్లుల్లి లేదా నిమ్మకాయ నూనెను ఉపయోగించండి. అవసరమైతే థయోఫెనేట్-మిథైల్ ఫంగిసైడ్‌ను ప్రయోగించండి.',
            'క్లోరోథాలోనిల్ (తక్కువ), థయోఫెనేట్-మిథైల్ (మధ్యస్థ), డైఫెనోకోనాజోల్ (అధిక)'),
        'Yellow Leaf Curl Virus': ('పసుపు ఆకుల మడత వైరస్',
            'రోగనిరోధక విత్తనాలను నాటండి. పచ్చని ఆకుల వైరస్ వ్యాప్తి నుండి నివారించడానికి తెల్ల దోమలను నియంత్రించండి.',
            'రసాయన చికిత్స లేదు')
    }
}

# ✅ Function to predict disease from uploaded image
def predict_disease(img, language):
    img = img.resize((256, 256))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = tomato_model.predict(img_array)
    predicted_class = class_labels[np.argmax(prediction)]

    disease_name, remedies, pesticides = translations.get(language, translations["English"]).get(predicted_class, ("Unknown", "No information available", "No pesticide needed"))

    return img, disease_name, remedies, pesticides

# ✅ Launch Gradio interface
iface = gr.Interface(
    fn=predict_disease,
    inputs=[gr.Image(type="pil"), gr.Dropdown(['English', 'Hindi', 'Telugu'], label="Select Language")],
    outputs=[gr.Image(), gr.Textbox(label="Disease Name"), gr.Textbox(label="Natural Remedies"), gr.Textbox(label="Recommended Pesticides")],
    title="Tomato Disease Detection"
)
iface.launch(
    server_name="0.0.0.0",
    server_port=7860
)
