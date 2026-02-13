"""Check pickle protocol version of model file"""
import pickle
import sys

print(f"Python version: {sys.version}")

model_file = "models/electricbills_predict.pkl"

try:
    with open(model_file, 'rb') as f:
        # Read pickle protocol
        first_byte = f.read(1)
        f.seek(0)
        
        # Try to determine protocol
        data = f.read(2)
        if len(data) >= 2:
            if data[0] == 0x80:  # Protocol 2+
                protocol = data[1]
                print(f"Pickle protocol version: {protocol}")
            else:
                print(f"Pickle protocol: 0 or 1 (text mode)")
        
        # Try to load
        f.seek(0)
        obj = pickle.load(f)
        print(f"✓ Model loaded successfully")
        print(f"Model type: {type(obj)}")
        
except Exception as e:
    print(f"✗ Error: {e}")
