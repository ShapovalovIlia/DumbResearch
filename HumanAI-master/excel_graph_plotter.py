import os
import pandas as pd
import matplotlib.pyplot as plt

class ExcelGraphPlotter:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def plot_graphs(self):
        """
        Plot the emotion data from each Excel file into a graph and save it with a name matching the original JSON file.
        Each Excel file's data is plotted in a 2x4 grid. Timestamps are not labeled on the x-axis.
        """
        files = os.listdir(self.folder_path)
        emotions = ["admiration", "adoration", "aestheticAppreciation", "amusement", "anger", "anxiety", "awe",
                    "awkwardness", "boredom", "calmness", "concentration", "confusion", "contemplation", "contempt",
                    "contentment", "craving", "desire", "determination", "disappointment", "disgust", "distress",
                    "doubt", "ecstasy", "embarrassment", "empathicPain", "entrancement", "envy", "excitement", "fear",
                    "guilt", "horror", "interest", "joy", "love", "nostalgia", "pain", "pride", "realization", "relief",
                    "romance", "sadness", "satisfaction", "shame", "surpriseNegative", "surprisePositive", "sympathy",
                    "tiredness", "triumph"]

        for file in files:
            if file.endswith('.xlsx'):
                df = pd.read_excel(os.path.join(self.folder_path, file))
                fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 20))
                axes = axes.flatten()

                # Plot each emotion in groups of 7 per subplot, without legend and without x-axis labels
                for i, ax in enumerate(axes[:-1]):  # Ignore the last subplot for now
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    for emotion in emotions[start_idx:end_idx]:
                        ax.plot(df['Timestamp'], df[emotion])
                    ax.set_title(f'Graph {i + 1}')
                    ax.tick_params(labelbottom=False)  # Hide x-axis labels

                # Hide the last subplot if it's unused
                if len(axes) % len(emotions) != 0:
                    axes[-1].axis('off')

                output_filename = f"{os.path.splitext(file)[0]}_emotions_grid.png"
                output_path = os.path.join(self.folder_path, output_filename)
                plt.tight_layout()
                plt.savefig(output_path)
                plt.close()
                print(f"Graph saved as {output_path}")
