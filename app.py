from flask import Flask, request, render_template, jsonify
from transformers import pipeline
import re
import os
import json
from data_loader import load_astronomy_dataset

app = Flask(__name__)

# Load a pre-trained question-answering model
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Load enhanced knowledge base
try:
    with open('enhanced_knowledge.json', 'r') as f:
        enhanced_knowledge = json.load(f)
    print(f"Loaded {len(enhanced_knowledge)} enhanced knowledge items")
except FileNotFoundError:
    print("Enhanced knowledge base not found, downloading dataset...")
    enhanced_knowledge = load_astronomy_dataset()
    if not enhanced_knowledge:
        enhanced_knowledge = {}
        print("Warning: Could not load enhanced knowledge base")

# Comprehensive astronomy knowledge base
astronomy_knowledge = {
    "Basic Concepts": {
        "What is the speed of light?": "The speed of light in a vacuum is approximately 299,792 kilometers per second (186,282 miles per second).",
        "How far is the Moon from Earth?": "The average distance from the Moon to Earth is approximately 384,400 kilometers (238,855 miles).",
        "What is a galaxy?": "A galaxy is a massive system of stars, stellar remnants, interstellar gas, dust, and dark matter, bound together by gravity.",
        "How many galaxies are in the observable universe?": "There are estimated to be around 2 trillion galaxies in the observable universe."
    },
    "Solar System": {
        "What is the largest planet in the Solar System?": "The largest planet in the Solar System is Jupiter.",
        "What is the hottest planet in the Solar System?": "Venus is the hottest planet in the Solar System due to its thick atmosphere that traps heat.",
        "What is an asteroid?": "An asteroid is a small rocky body that orbits the Sun, mostly found in the asteroid belt between Mars and Jupiter.",
        "What is a comet?": "A comet is a small solar system body made of ice, dust, and rock that develops a glowing coma and tail when it approaches the Sun.",
        "What is the Kuiper Belt?": "The Kuiper Belt is a region of the Solar System beyond Neptune that contains many small icy bodies and dwarf planets.",
        "What is the Oort Cloud?": "The Oort Cloud is a hypothetical, distant cloud of icy objects surrounding the Solar System and is believed to be the source of long-period comets.",
        "What is the Solar System?": "The Solar System consists of the Sun and all celestial objects bound to it by gravity, including planets, dwarf planets, moons, asteroids, comets, and other objects.",
        "How old is the Solar System?": "The Solar System formed approximately 4.6 billion years ago from the gravitational collapse of a giant molecular cloud.",
        "How many planets are in the Solar System?": "There are eight official planets in our Solar System: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune. Pluto was reclassified as a dwarf planet in 2006.",
        "Tell me about Mercury": "Mercury is the smallest and innermost planet in the Solar System. It has no moons, no substantial atmosphere, and orbits the Sun every 88 Earth days. Its surface is heavily cratered, similar to Earth's Moon.",
        "Tell me about Venus": "Venus is the second planet from the Sun and is Earth's closest planetary neighbor. It's often called Earth's twin because of their similar size, but Venus has a toxic atmosphere and surface temperatures that can melt lead.",
        "Tell me about Mars": "Mars is the fourth planet from the Sun and is known as the Red Planet due to its reddish appearance. It has two small moons, thin atmosphere, and shows evidence of ancient river valleys and water activity."
    },
    "Stars and Galaxies": {
        "What are pulsars?": "Pulsars are highly magnetized, rotating neutron stars that emit beams of electromagnetic radiation.",
        "What is a star?": "A star is a luminous spheroid of plasma held together by its own gravity. The nearest star to Earth is the Sun.",
        "What is the Milky Way?": "The Milky Way is our home galaxy, a large spiral galaxy containing hundreds of billions of stars, including our Sun.",
        "How do stars form?": "Stars form within molecular clouds of gas and dust. These clouds collapse under gravity, forming denser regions that eventually become stars.",
        "What is a supernova?": "A supernova is the explosive death of a star, which can briefly outshine an entire galaxy. It occurs either when a massive star runs out of nuclear fuel or when a white dwarf accumulates too much matter from a companion star.",
        "What is a neutron star?": "A neutron star is the incredibly dense core left behind after a massive star explodes as a supernova. A teaspoon of neutron star material would weigh billions of tons.",
        "What are constellations?": "Constellations are patterns of stars that form recognizable shapes and have been used for navigation and storytelling throughout human history. There are 88 officially recognized constellations."
    },
    "Space Phenomena": {
        "What is a nebula?": "A nebula is a giant cloud of dust and gas in space, often the birthplace of stars.",
        "What is a black hole?": "A black hole is a region of spacetime where gravity is so strong that nothing, including light, can escape from it once it passes the event horizon.",
        "What is dark matter?": "Dark matter is a hypothetical form of matter thought to account for approximately 85% of the matter in the universe and about 27% of its total mass-energy content.",
        "What causes a solar eclipse?": "A solar eclipse occurs when the Moon passes between Earth and the Sun, thereby obscuring Earth's view of the Sun totally or partially.",
        "What is dark energy?": "Dark energy is a mysterious force that appears to be causing the universe to expand at an accelerating rate. It accounts for about 68% of the universe's total energy.",
        "What is a meteor shower?": "A meteor shower occurs when Earth passes through debris left behind by a comet or asteroid. This debris burns up in Earth's atmosphere, creating streaks of light in the night sky.",
        "What is the aurora borealis?": "The aurora borealis (Northern Lights) is a natural light display caused by charged particles from the Sun interacting with Earth's magnetic field and atmosphere."
    },
    "Space Exploration": {
        "Can humans live on Mars?": "Currently, humans cannot live on Mars due to its harsh conditions, but space agencies are researching future missions and technologies that might make Mars habitation possible.",
        "What is NASA?": "NASA (National Aeronautics and Space Administration) is an independent agency of the U.S. federal government responsible for the civilian space program, aeronautics research, and space research.",
        "What is the ISS?": "The International Space Station (ISS) is a modular space station in low Earth orbit. It's a multinational collaborative project involving NASA, Roscosmos, ESA, JAXA, and CSA.",
        "What was the Apollo program?": "The Apollo program was a NASA space program that achieved landing the first humans on the Moon with Apollo 11 in 1969.",
        "What is SpaceX?": "SpaceX is a private space company founded by Elon Musk that develops and launches advanced rockets and spacecraft. It's known for its reusable rockets and plans for Mars colonization.",
        "What is the James Webb Space Telescope?": "The James Webb Space Telescope is the largest and most powerful space telescope ever built. It observes the universe in infrared light, allowing it to see through cosmic dust and study distant galaxies.",
        "What is the Artemis program?": "The Artemis program is NASA's plan to return humans to the Moon and establish a sustainable presence there, with the ultimate goal of using it as a stepping stone for human missions to Mars."
    },
    "Astronomical Discoveries": {
        "How are exoplanets detected?": "Exoplanets are primarily detected using methods like the transit method, where a planet passes in front of its star, and the radial velocity method, which measures the star's wobble due to the planet's gravity.",
        "What is the Big Bang?": "The Big Bang theory suggests that the universe began about 13.8 billion years ago from an infinitely dense point, expanding rapidly to form the cosmos we see today.",
        "What are exoplanets?": "Exoplanets are planets that orbit stars other than our Sun. Thousands have been discovered, and some may have conditions suitable for life.",
        "What is the Hubble Space Telescope?": "The Hubble Space Telescope is a space-based observatory launched in 1990. It has made numerous groundbreaking discoveries and taken spectacular images of distant galaxies, nebulae, and other cosmic objects.",
        "What is the Golden Record?": "The Golden Record is a phonograph record launched with the Voyager spacecraft in 1977, containing sounds and images of Earth for any extraterrestrial intelligence that might find it.",
        "What are gravitational waves?": "Gravitational waves are ripples in spacetime caused by massive cosmic events like colliding black holes. They were first directly detected in 2015, confirming Einstein's theory of general relativity."
    }
}

def get_best_answer(question):
    try:
        print(f"Received question: {question}")
        
        # Combine all knowledge into a single context
        all_knowledge = ""
        
        # First try enhanced knowledge base
        if enhanced_knowledge:
            # Try exact match in enhanced knowledge
            cleaned_question = re.sub(r'[^\w\s?]', '', question.lower())
            print(f"Cleaned question: {cleaned_question}")
            
            # Try direct matching with enhanced knowledge
            for q, a in enhanced_knowledge.items():
                if cleaned_question in q.lower() or q.lower() in cleaned_question:
                    print(f"Found direct match in enhanced knowledge: {q}")
                    return a, True
            
            # Add enhanced knowledge to context
            all_knowledge += " ".join(enhanced_knowledge.values()) + " "
        
        # Add base knowledge to context
        for category in astronomy_knowledge.values():
            all_knowledge += " ".join(category.values()) + " "
            # Try direct matching with base knowledge
            for q, a in category.items():
                if cleaned_question in q.lower() or q.lower() in cleaned_question:
                    print(f"Found direct match in base knowledge: {q}")
                    return a, True

        # If no direct match, use the QA pipeline
        print("No direct match found, using QA pipeline")
        result = qa_pipeline(
            question=cleaned_question,
            context=all_knowledge,
            max_answer_length=100
        )

        print(f"QA pipeline result: {result}")
        return result['answer'], True

    except Exception as e:
        print(f"Error in get_best_answer: {str(e)}")
        return str(e), False

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    question = None
    answer = None
    categories = list(astronomy_knowledge.keys())

    if request.method == 'POST':
        question = request.form.get('question')
        if not question:
            error = "Please enter a question"
        else:
            answer, success = get_best_answer(question)
            if not success:
                error = "Sorry, I couldn't generate an answer. Please try again."

    return render_template('index.html',
                         question=question,
                         answer=answer,
                         error=error,
                         categories=categories)

@app.route('/api/ask', methods=['POST'])
def api_ask():
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question.strip():
            return jsonify({'error': 'Please provide a question'}), 400

        answer, success = get_best_answer(question)
        if not success:
            return jsonify({'error': 'Failed to generate answer'}), 500

        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host='0.0.0.0', port=port, debug=debug)
