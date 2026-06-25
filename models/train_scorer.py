import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from .lead_scorer import get_model

MODEL_PATH = os.path.join(os.path.dirname(__file__), "lead_scorer.pt")

def generate_synthetic_data(num_samples=500):
    # Features:
    # 0: student_strength_norm (0-1)
    # 1: institution_type_encoded (0-1)
    # 2: has_prior_partnership (0 or 1)
    # 3: program_interest_match (0-1)
    # 4: lead_source_score (0-1)
    # 5: contact_seniority_score (0-1)
    # 6: days_since_created (normalized 0-1)
    # 7: follow_up_count (normalized 0-1)
    
    np.random.seed(42)
    torch.manual_seed(42)
    
    X = np.random.rand(num_samples, 8).astype(np.float32)
    # Make some logic for the target y
    # High score if strong match, prior partnership, strong source, seniority
    y = 0.2 * X[:, 0] + 0.1 * X[:, 1] + 0.3 * X[:, 2] + 0.2 * X[:, 3] + \
        0.1 * X[:, 4] + 0.1 * X[:, 5] - 0.1 * X[:, 6] + 0.1 * X[:, 7]
    
    # Add noise
    y += np.random.normal(0, 0.05, num_samples)
    y = np.clip(y, 0, 1).astype(np.float32)
    
    return torch.tensor(X), torch.tensor(y).unsqueeze(1)

def train_and_save_model():
    if os.path.exists(MODEL_PATH):
        print("Model already trained and exists.")
        return

    print("Training PyTorch lead scoring model...")
    X, y = generate_synthetic_data(500)
    
    model = get_model()
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    epochs = 100
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        
        if (epoch+1) % 20 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')
            
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
