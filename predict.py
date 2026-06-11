<<<<<<< HEAD
import gradio as gr
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model("C:/Users/gakil/Searches/OneDrive/Desktop/tomato_disease_model.h5")

# Define class labels (order should match your dataset classes)
class_labels = ['Bacterial Spot', 'Early Blight', 'Healthy', 'Late Blight', 'Septoria Leaf Spot', 'Yellow Leaf Curl Virus']

# Disease translations for each language
disease_translations = {
    'English': {
        'Bacterial Spot': 'Bacterial Spot',
        'Early Blight': 'Early Blight',
        'Healthy': 'Healthy',
        'Late Blight': 'Late Blight',
        'Septoria Leaf Spot': 'Septoria Leaf Spot',
        'Yellow Leaf Curl Virus': 'Yellow Leaf Curl Virus',
    },
    'Hindi': {
        'Bacterial Spot': 'बैक्टीरियल धब्बा',
        'Early Blight': 'प्रारंभिक मुरझाना',
        'Healthy': 'स्वस्थ',
        'Late Blight': 'देर से मुरझाना',
        'Septoria Leaf Spot': 'सेप्टोरिया पत्ते का धब्बा',
        'Yellow Leaf Curl Virus': 'पीला पत्ते मरोड़ वायरस',
    },
    'Telugu': {
        'Bacterial Spot': 'బ్యాక్టీరియల్ స్పాట్',
        'Early Blight': 'ప్రారంభ మురి',
        'Healthy': 'ఆరోగ్యకరమైన',
        'Late Blight': 'విలంబిత మురి',
        'Septoria Leaf Spot': 'సెప్టోరియా ఆకు ప్రదేశం',
        'Yellow Leaf Curl Virus': 'పసుపు ఆకు ముడులు వైరస్',
    }
}

# Remedies and pesticide translations
remedies_translations = {
    'English': {
        'Bacterial Spot': 'Use garlic spray for natural antibacterial properties. Apply neem oil solution to reduce bacterial growth.',
        'Early Blight': 'Use a copper-based fungicide. Apply organic fungicide sprays like neem oil.',
        'Healthy': 'Maintain healthy plant care with proper watering and sunlight.',
        'Late Blight': 'Remove infected leaves and apply fungicide sprays.',
        'Septoria Leaf Spot': 'Use copper-based fungicides to control leaf spots.',
        'Yellow Leaf Curl Virus': 'Use insecticides to control the vector. Remove affected leaves.',
    },
    'Hindi': {
        'Bacterial Spot': 'प्राकृतिक जीवाणुरोधी गुणों के लिए लहसुन स्प्रे का उपयोग करें। बैक्टीरियल वृद्धि को कम करने के लिए नीम तेल घोल लगाएं।',
        'Early Blight': 'कॉपर-आधारित फंगीसाइड का उपयोग करें। जैविक फंगीसाइड स्प्रे जैसे नीम तेल का उपयोग करें।',
        'Healthy': 'सही पानी और सूर्य प्रकाश के साथ स्वस्थ पौधों की देखभाल करें।',
        'Late Blight': 'संक्रमित पत्तियों को हटा दें और फंगीसाइड स्प्रे लगाएं।',
        'Septoria Leaf Spot': 'पत्ते के धब्बों को नियंत्रित करने के लिए कॉपर-आधारित फंगीसाइड का उपयोग करें।',
        'Yellow Leaf Curl Virus': 'किटाणु को नियंत्रित करने के लिए कीटनाशक का उपयोग करें। प्रभावित पत्तियों को हटा दें।',
    },
    'Telugu': {
        'Bacterial Spot': 'ప్రाकृतिक జీవాణు నిరోధక లక్షణాల కోసం వెల్లుల్లి స్ప్రే ఉపయోగించండి. బ్యాక్టీరియల్ వృద్ధిని తగ్గించడానికి నిమ్మ तेल ద్రావణం ఉపయోగించండి.',
        'Early Blight': 'కాపర్-ఆధారిత ఫంగిసైడ్ ఉపయోగించండి. జైవిక ఫంగిసైడ్ స్ప్రేలు లాంటి నిమ్మ तेल ఉపయోగించండి.',
        'Healthy': 'సరైన నీటినీ మరియు సూర్యరశ్మి తో ఆరోగ్యకరమైన మొక్కల జాగ్రత్త తీసుకోండి.',
        'Late Blight': 'ప్రభావిత పసుపు ఆకులను తొలగించి ఫంగిసైడ్ స్ప్రే చేయండి.',
        'Septoria Leaf Spot': 'ఆకుల పగుళ్లను నియంత్రించడానికి కాపర్-ఆధారిత ఫంగిసైడ్ ఉపయోగించండి.',
        'Yellow Leaf Curl Virus': 'వైరస్ వ్యాప్తి నిరోధించడానికి పునరావృత యాంటివైరల్ మందులు ఉపయోగించండి.',
    }
}

pesticides_translations = {
    'English': {
        'Bacterial Spot': 'Low strength: Copper-based fungicides. Medium strength: Streptomycin. High strength: Oxytetracycline.',
        'Early Blight': 'Low strength: Neem oil. Medium strength: Mancozeb. High strength: Chlorothalonil.',
        'Healthy': 'No pesticide needed.',
        'Late Blight': 'Low strength: Copper-based fungicides. Medium strength: Chlorothalonil. High strength: Metalaxyl.',
        'Septoria Leaf Spot': 'Low strength: Copper fungicides. Medium strength: Mancozeb. High strength: Propiconazole.',
        'Yellow Leaf Curl Virus': 'No pesticide needed.',
    },
    'Hindi': {
        'Bacterial Spot': 'कम ताकत: तांबे-आधारित कवकनाशी। मध्यम ताकत: स्ट्रेप्टोमाइसिन। उच्च ताकत: ऑक्सीटेट्रासाइक्लिन।',
        'Early Blight': 'कम ताकत: नीम तेल। मध्यम ताकत: मैनकोजेब। उच्च ताकत: क्लोरोथैलोनिल।',
        'Healthy': 'कोई कीटनाशक नहीं चाहिए।',
        'Late Blight': 'कम ताकत: तांबे-आधारित कवकनाशी। मध्यम ताकत: क्लोरोथैलोनिल। उच्च ताकत: मेटालाक्सिल।',
        'Septoria Leaf Spot': 'कम ताकत: तांबे कवकनाशी। मध्यम ताकत: मैनकोजेब। उच्च ताकत: प्रोपिकोनाज़ोल।',
        'Yellow Leaf Curl Virus': 'कोई कीटनाशक नहीं चाहिए।',
    },
    'Telugu': {
        'Bacterial Spot': 'తక్కువ శక్తి: కాపర్-ఆధారిత ఫంగిసైడ్స్. మధ్యస్థ శక్తి: స్ట్రెప్టోమైసిన్. అధిక శక్తి: ఆక్సిటెట్రాసైక్లిన్.',
        'Early Blight': 'తక్కువ శక్తి: నిమ్మ तेल. మధ్యస్థ శక్తి: మాంకోజెబ్. అధిక శక్తి: క్లొరొథలొనిల్.',
        'Healthy': 'ఎటువంటి పురుగుల మందు అవసరం లేదు.',
        'Late Blight': 'తక్కువ శక్తి: కాపర్-ఆధారిత ఫంగిసైడ్స్. మధ్యస్థ శక్తి: క్లొరొథలొనిల్. అధిక శక్తి: మెటాలాక్సిల్.',
        'Septoria Leaf Spot': 'తక్కువ శక్తి: కాపర్ ఫంగిసైడ్స్. మధ్యస్థ శక్తి: మాంకోజెబ్. అధిక శక్తి: ప్రోపికొనాజోల్.',
        'Yellow Leaf Curl Virus': 'ఎటువంటి పురుగుల మందు అవసరం లేదు.',
    }
}

# Function to preprocess the image and make predictions
def predict_disease(img, language):
    img = img.resize((256, 256))  # Resize to match model input
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict disease probabilities
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])  # Get the index of the highest probability class

    predicted_disease = class_labels[predicted_class]
    translated_disease = disease_translations[language].get(predicted_disease, predicted_disease)
    remedy = remedies_translations[language].get(predicted_disease, "No remedy available.")
    pesticide = pesticides_translations[language].get(predicted_disease, "No pesticide needed.")

    return img, translated_disease, remedy, pesticide

# Create Gradio interface
iface = gr.Interface(
    fn=predict_disease,
    inputs=[gr.Image(type="pil", label="Upload a Tomato Leaf Image"),
            gr.Dropdown(choices=['English', 'Hindi', 'Telugu'], label="Select Language")],
    outputs=[gr.Image(label="Uploaded Image"),
             gr.Textbox(label="Predicted Disease"),
             gr.Textbox(label="Remedy Suggestion"),
             gr.Textbox(label="Pesticide Recommendation")],
)

iface.launch(share=True)
=======
import gradio as gr
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load the trained model
model = tf.keras.models.load_model("C:/Users/gakil/Searches/OneDrive/Desktop/tomato_disease_model.h5")

# Define class labels (order should match your dataset classes)
class_labels = ['Bacterial Spot', 'Early Blight', 'Healthy', 'Late Blight', 'Septoria Leaf Spot', 'Yellow Leaf Curl Virus']

# Disease translations for each language
disease_translations = {
    'English': {
        'Bacterial Spot': 'Bacterial Spot',
        'Early Blight': 'Early Blight',
        'Healthy': 'Healthy',
        'Late Blight': 'Late Blight',
        'Septoria Leaf Spot': 'Septoria Leaf Spot',
        'Yellow Leaf Curl Virus': 'Yellow Leaf Curl Virus',
    },
    'Hindi': {
        'Bacterial Spot': 'बैक्टीरियल धब्बा',
        'Early Blight': 'प्रारंभिक मुरझाना',
        'Healthy': 'स्वस्थ',
        'Late Blight': 'देर से मुरझाना',
        'Septoria Leaf Spot': 'सेप्टोरिया पत्ते का धब्बा',
        'Yellow Leaf Curl Virus': 'पीला पत्ते मरोड़ वायरस',
    },
    'Telugu': {
        'Bacterial Spot': 'బ్యాక్టీరియల్ స్పాట్',
        'Early Blight': 'ప్రారంభ మురి',
        'Healthy': 'ఆరోగ్యకరమైన',
        'Late Blight': 'విలంబిత మురి',
        'Septoria Leaf Spot': 'సెప్టోరియా ఆకు ప్రదేశం',
        'Yellow Leaf Curl Virus': 'పసుపు ఆకు ముడులు వైరస్',
    }
}

# Remedies and pesticide translations
remedies_translations = {
    'English': {
        'Bacterial Spot': 'Use garlic spray for natural antibacterial properties. Apply neem oil solution to reduce bacterial growth.',
        'Early Blight': 'Use a copper-based fungicide. Apply organic fungicide sprays like neem oil.',
        'Healthy': 'Maintain healthy plant care with proper watering and sunlight.',
        'Late Blight': 'Remove infected leaves and apply fungicide sprays.',
        'Septoria Leaf Spot': 'Use copper-based fungicides to control leaf spots.',
        'Yellow Leaf Curl Virus': 'Use insecticides to control the vector. Remove affected leaves.',
    },
    'Hindi': {
        'Bacterial Spot': 'प्राकृतिक जीवाणुरोधी गुणों के लिए लहसुन स्प्रे का उपयोग करें। बैक्टीरियल वृद्धि को कम करने के लिए नीम तेल घोल लगाएं।',
        'Early Blight': 'कॉपर-आधारित फंगीसाइड का उपयोग करें। जैविक फंगीसाइड स्प्रे जैसे नीम तेल का उपयोग करें।',
        'Healthy': 'सही पानी और सूर्य प्रकाश के साथ स्वस्थ पौधों की देखभाल करें।',
        'Late Blight': 'संक्रमित पत्तियों को हटा दें और फंगीसाइड स्प्रे लगाएं।',
        'Septoria Leaf Spot': 'पत्ते के धब्बों को नियंत्रित करने के लिए कॉपर-आधारित फंगीसाइड का उपयोग करें।',
        'Yellow Leaf Curl Virus': 'किटाणु को नियंत्रित करने के लिए कीटनाशक का उपयोग करें। प्रभावित पत्तियों को हटा दें।',
    },
    'Telugu': {
        'Bacterial Spot': 'ప్రाकृतिक జీవాణు నిరోధక లక్షణాల కోసం వెల్లుల్లి స్ప్రే ఉపయోగించండి. బ్యాక్టీరియల్ వృద్ధిని తగ్గించడానికి నిమ్మ तेल ద్రావణం ఉపయోగించండి.',
        'Early Blight': 'కాపర్-ఆధారిత ఫంగిసైడ్ ఉపయోగించండి. జైవిక ఫంగిసైడ్ స్ప్రేలు లాంటి నిమ్మ तेल ఉపయోగించండి.',
        'Healthy': 'సరైన నీటినీ మరియు సూర్యరశ్మి తో ఆరోగ్యకరమైన మొక్కల జాగ్రత్త తీసుకోండి.',
        'Late Blight': 'ప్రభావిత పసుపు ఆకులను తొలగించి ఫంగిసైడ్ స్ప్రే చేయండి.',
        'Septoria Leaf Spot': 'ఆకుల పగుళ్లను నియంత్రించడానికి కాపర్-ఆధారిత ఫంగిసైడ్ ఉపయోగించండి.',
        'Yellow Leaf Curl Virus': 'వైరస్ వ్యాప్తి నిరోధించడానికి పునరావృత యాంటివైరల్ మందులు ఉపయోగించండి.',
    }
}

pesticides_translations = {
    'English': {
        'Bacterial Spot': 'Low strength: Copper-based fungicides. Medium strength: Streptomycin. High strength: Oxytetracycline.',
        'Early Blight': 'Low strength: Neem oil. Medium strength: Mancozeb. High strength: Chlorothalonil.',
        'Healthy': 'No pesticide needed.',
        'Late Blight': 'Low strength: Copper-based fungicides. Medium strength: Chlorothalonil. High strength: Metalaxyl.',
        'Septoria Leaf Spot': 'Low strength: Copper fungicides. Medium strength: Mancozeb. High strength: Propiconazole.',
        'Yellow Leaf Curl Virus': 'No pesticide needed.',
    },
    'Hindi': {
        'Bacterial Spot': 'कम ताकत: तांबे-आधारित कवकनाशी। मध्यम ताकत: स्ट्रेप्टोमाइसिन। उच्च ताकत: ऑक्सीटेट्रासाइक्लिन।',
        'Early Blight': 'कम ताकत: नीम तेल। मध्यम ताकत: मैनकोजेब। उच्च ताकत: क्लोरोथैलोनिल।',
        'Healthy': 'कोई कीटनाशक नहीं चाहिए।',
        'Late Blight': 'कम ताकत: तांबे-आधारित कवकनाशी। मध्यम ताकत: क्लोरोथैलोनिल। उच्च ताकत: मेटालाक्सिल।',
        'Septoria Leaf Spot': 'कम ताकत: तांबे कवकनाशी। मध्यम ताकत: मैनकोजेब। उच्च ताकत: प्रोपिकोनाज़ोल।',
        'Yellow Leaf Curl Virus': 'कोई कीटनाशक नहीं चाहिए।',
    },
    'Telugu': {
        'Bacterial Spot': 'తక్కువ శక్తి: కాపర్-ఆధారిత ఫంగిసైడ్స్. మధ్యస్థ శక్తి: స్ట్రెప్టోమైసిన్. అధిక శక్తి: ఆక్సిటెట్రాసైక్లిన్.',
        'Early Blight': 'తక్కువ శక్తి: నిమ్మ तेल. మధ్యస్థ శక్తి: మాంకోజెబ్. అధిక శక్తి: క్లొరొథలొనిల్.',
        'Healthy': 'ఎటువంటి పురుగుల మందు అవసరం లేదు.',
        'Late Blight': 'తక్కువ శక్తి: కాపర్-ఆధారిత ఫంగిసైడ్స్. మధ్యస్థ శక్తి: క్లొరొథలొనిల్. అధిక శక్తి: మెటాలాక్సిల్.',
        'Septoria Leaf Spot': 'తక్కువ శక్తి: కాపర్ ఫంగిసైడ్స్. మధ్యస్థ శక్తి: మాంకోజెబ్. అధిక శక్తి: ప్రోపికొనాజోల్.',
        'Yellow Leaf Curl Virus': 'ఎటువంటి పురుగుల మందు అవసరం లేదు.',
    }
}

# Function to preprocess the image and make predictions
def predict_disease(img, language):
    img = img.resize((256, 256))  # Resize to match model input
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Predict disease probabilities
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])  # Get the index of the highest probability class

    predicted_disease = class_labels[predicted_class]
    translated_disease = disease_translations[language].get(predicted_disease, predicted_disease)
    remedy = remedies_translations[language].get(predicted_disease, "No remedy available.")
    pesticide = pesticides_translations[language].get(predicted_disease, "No pesticide needed.")

    return img, translated_disease, remedy, pesticide

# Create Gradio interface
iface = gr.Interface(
    fn=predict_disease,
    inputs=[gr.Image(type="pil", label="Upload a Tomato Leaf Image"),
            gr.Dropdown(choices=['English', 'Hindi', 'Telugu'], label="Select Language")],
    outputs=[gr.Image(label="Uploaded Image"),
             gr.Textbox(label="Predicted Disease"),
             gr.Textbox(label="Remedy Suggestion"),
             gr.Textbox(label="Pesticide Recommendation")],
)

iface.launch(share=True)
>>>>>>> 55f015d0840e17926785313512fef6048d0d9875
