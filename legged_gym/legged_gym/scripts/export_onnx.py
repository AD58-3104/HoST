# export_onnx.py
import sys
import torch
import torch.nn as nn
import onnxruntime as ort
import numpy as np

if len(sys.argv) < 2:
    print("Usage: python export_onnx.py <path_to_checkpoint>")
    sys.exit(1)

ckpt_path = sys.argv[1]
output_path = sys.argv[2] if len(sys.argv) >= 3 else 'policy.onnx'

# Actorネットワーク再構築
actor = nn.Sequential(
    nn.Linear(438, 512), nn.ELU(),
    nn.Linear(512, 256), nn.ELU(),
    nn.Linear(256, 128), nn.ELU(),
    nn.Linear(128, 22)
)

# weightsだけ抽出してロード
ckpt = torch.load(ckpt_path, map_location='cpu')
sd = ckpt['model_state_dict']
actor_sd = {
    '0.weight': sd['actor.0.weight'],
    '0.bias':   sd['actor.0.bias'],
    '2.weight': sd['actor.2.weight'],
    '2.bias':   sd['actor.2.bias'],
    '4.weight': sd['actor.4.weight'],
    '4.bias':   sd['actor.4.bias'],
    '6.weight': sd['actor.6.weight'],
    '6.bias':   sd['actor.6.bias'],
}
actor.load_state_dict(actor_sd)
actor.eval()

# ONNX export
dummy = torch.zeros(1, 438)
torch.onnx.export(
    actor, dummy, output_path,
    input_names=['obs'],
    output_names=['actions'],
    opset_version=11,
    dynamic_axes={'obs': {0: 'batch_size'}, 'actions': {0: 'batch_size'}}
)
print(f"Done: {output_path}")

# 動作確認
sess = ort.InferenceSession(output_path)
out = sess.run(None, {'obs': np.zeros((1, 438), dtype=np.float32)})
print("Output shape:", out[0].shape)