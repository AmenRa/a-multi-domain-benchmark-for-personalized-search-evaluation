MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
EMD_DIM=384
BATCH=64
N_EPOCHS=10
FOLDER=../datasets/physics
SEED=42
ACRONYM=phy
MODEL_OUTPUT=../outputs/mini_${ACRONYM}_saved_models
LAST_MODEL=../outputs/mini_${ACRONYM}_saved_models/model_10.pt
EMB_OUT=../outputs/${ACRONYM}_embeddings


python train.py --domain_path $FOLDER --n_epochs $N_EPOCHS --batch_size $BATCH --bert_name $MODEL_NAME --seed $SEED --output_folder $MODEL_OUTPUT
python create_embedding_matrix.py --domain_path $FOLDER --bert_name $MODEL_NAME --embedding_dim $EMD_DIM --model_path $LAST_MODEL --output $EMB_OUT
python testing.py --embedding_folder $EMB_OUT --bert_name $MODEL_NAME --model_path $LAST_MODEL --domain_path $FOLDER --split val
