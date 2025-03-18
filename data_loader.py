import kagglehub
import pandas as pd
import json

def load_astronomy_dataset():
    """
    Download and process the astronomical dataset from Kaggle
    """
    try:
        # Download the dataset
        print("Downloading dataset...")
        path = kagglehub.dataset_download("devendrasingh22/astronomical-data")
        print(f"Dataset downloaded to: {path}")
        
        # Load the star data CSV
        csv_path = f"{path}/cleaned_star_data.csv"
        print(f"Loading data from: {csv_path}")
        stars_df = pd.read_csv(csv_path)
        print(f"Loaded {len(stars_df)} star records")
        print(f"Columns in dataset: {stars_df.columns.tolist()}")
        print(f"First row of data:\n{stars_df.iloc[0]}")
        
        # Process star data
        knowledge_base = {}
        
        # Add general star information
        for idx, row in stars_df.iterrows():
            # Generate a unique star name since the dataset doesn't have names
            name = f"Star_{idx+1}"
            
            # Basic information about the star
            question = f"Tell me about {name}"
            answer = f"{name} is a star with "
            
            # Add temperature information
            if pd.notna(row['Temperature (K)']):
                temp = row['Temperature (K)']
                answer += f"a surface temperature of {temp:,.0f} Kelvin. "
                knowledge_base[f"What is the temperature of {name}?"] = f"The surface temperature of {name} is {temp:,.0f} Kelvin."
            
            # Add luminosity information
            if pd.notna(row['Luminosity(L/Lo)']):
                lum = row['Luminosity(L/Lo)']
                answer += f"Its luminosity is {lum:,.2f} times that of the Sun. "
                knowledge_base[f"What is the luminosity of {name}?"] = f"The luminosity of {name} is {lum:,.2f} times that of the Sun."
            
            # Add radius information
            if pd.notna(row['Radius(R/Ro)']):
                radius = row['Radius(R/Ro)']
                answer += f"The star's radius is {radius:,.2f} times that of the Sun. "
                knowledge_base[f"What is the radius of {name}?"] = f"The radius of {name} is {radius:,.2f} times that of the Sun."
            
            # Add star type and color
            if pd.notna(row['Star type']):
                answer += f"It is a {row['Star type']} star. "
                knowledge_base[f"What type of star is {name}?"] = f"{name} is a {row['Star type']} star."
            
            if pd.notna(row['Star color']):
                answer += f"The star appears {row['Star color'].lower()} in color. "
                knowledge_base[f"What color is {name}?"] = f"{name} appears {row['Star color'].lower()} in color."
            
            # Add spectral class
            if pd.notna(row['Spectral Class']):
                answer += f"It belongs to spectral class {row['Spectral Class']}."
                knowledge_base[f"What is the spectral class of {name}?"] = f"{name} belongs to spectral class {row['Spectral Class']}."
            
            knowledge_base[question] = answer.strip()
            
            # Break after first row for debugging
            if idx == 0:
                print(f"\nSample knowledge entries for {name}:")
                for q, a in knowledge_base.items():
                    print(f"Q: {q}")
                    print(f"A: {a}\n")
                break
        
        # Add some general knowledge about star types
        knowledge_base["What are the different types of stars?"] = "Stars are classified into several types based on their characteristics: Red Dwarf, Brown Dwarf, White Dwarf, Main Sequence, SuperGiants, and HyperGiants."
        knowledge_base["What are spectral classes?"] = "Spectral classes are categories used to classify stars based on their spectral characteristics. The main sequence goes O, B, A, F, G, K, M from hottest to coolest, with additional classes for special types of stars."
        
        # Save the enhanced knowledge base
        with open('enhanced_knowledge.json', 'w') as f:
            json.dump(knowledge_base, f, indent=2)
            
        print(f"Successfully processed {len(knowledge_base)} questions and answers")
        return knowledge_base
        
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return None

if __name__ == "__main__":
    load_astronomy_dataset()
