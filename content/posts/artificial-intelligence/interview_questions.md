# Topics

- imbalanced Classes
- overfitting
- underfitting
- neural networks
- interview questions

## ⚖️ Imbalanced Classes
What it is

- When one class dominates the dataset (e.g., 95% class A, 5% class B).

- Accuracy becomes misleading — predicting only the majority class gives high accuracy but useless results.

Why it matters

- Common in real-world: fraud detection, disease diagnosis, anomaly detection.

How to handle it

- Data-level approaches:

    - Oversampling minority (e.g., SMOTE).

    - Undersampling majority.

- Algorithm-level approaches:

    - Use class weights (heavier penalty on minority misclassification).

    - Cost-sensitive learning.

- Evaluation metrics:

    - Prefer Precision, Recall, F1, ROC-AUC, PR-AUC over Accuracy.

👉 Interview line: “With imbalanced data, I adjust sampling or class weights and focus on metrics like F1 or ROC-AUC, not just accuracy.”

## 🎭 Overfitting
What it is

- Model memorizes training data, including noise.

- Training accuracy ≫ Validation accuracy.

Causes

- Too complex model, too few samples, training too long.

Fixes

- Regularization (L1, L2, dropout).

- Early stopping.

- Simplify the model.

- Data augmentation (esp. in CV).

👉 Interview line: “Overfitting is high variance — I reduce it with regularization, dropout, early stopping, or more data.”

## 🌱 Underfitting

What it is

- Model is too simple to capture patterns.

- Training accuracy is low, validation accuracy also low.

Causes

- Oversimplified model.

- Too much regularization.

- Too little training.

Fixes

- Increase model complexity (deeper network, more features).

- Reduce regularization.

- Train longer / better learning rate.

👉 Interview line: “Underfitting is high bias — I fix it with a more complex model, more features, or longer training.”

## 🧠 Neural Networks (NNs)

What they are

- Inspired by the brain.

- Composed of layers of neurons (Input → Hidden → Output).

- Each neuron computes: weighted sum + bias → activation function.

How they learn

- Forward pass → compute output.

- Loss function → measure error.

- Backpropagation → compute gradients.

- Gradient descent → update weights.

Key architectures

- Feedforward (MLP) – classic, tabular data.

- CNNs – vision tasks, extract spatial features.

- RNNs / LSTMs – sequences, time-series, speech.

- Transformers – modern LLMs, attention mechanism.

👉 Interview line: “Neural networks stack layers of nonlinear transformations. They learn via backpropagation and gradient descent. CNNs for images, RNNs for sequences, Transformers for language.”

## 🔑 Likely Interview Questions

- “If you have a dataset with 99% negative and 1% positive, how do you evaluate your model?”

- “What’s the difference between overfitting and underfitting? How would you detect each?”

- “How does backpropagation work in a neural network?”

- “Why do we need activation functions in neural networks?”

- “How would you prevent overfitting in a deep learning model?”

### “If you have a dataset with 99% negative and 1% positive, how do you evaluate your model?”

Correct Interview Approach

1. Point out why accuracy is misleading

“If I use accuracy, the model could predict all negatives and still get 99%, but it would miss all positives — so it’s useless.”

2. Propose better metrics

- Precision = TP / (TP+FP) → how many predicted positives are correct.

- Recall (Sensitivity) = TP / (TP+FN) → how many actual positives the model catches.

- F1-score = harmonic mean of Precision & Recall.

- ROC-AUC = ability to distinguish classes.

- PR-AUC = especially important for highly skewed data.

3. Mention strategies to balance evaluation

- Use confusion matrix.

- Adjust decision threshold.

- Use class weights or sampling techniques.


Model Answer (you can say in the interview):

“In a dataset with 99% negatives and 1% positives, accuracy is misleading because predicting only negatives gives 99% accuracy but 0% recall. I would evaluate using metrics like Precision, Recall, F1-score, and ROC/PR-AUC. For example, in fraud detection, Recall is critical since missing a fraud is more costly than a few false positives.”

### “What’s the difference between overfitting and underfitting? How would you detect each?”

🔎 Difference

- Overfitting (high variance)

    - Model learns the training data too well, including noise.

    - Performs great on training data, poorly on unseen data.

    - Cause: model too complex, too many parameters, too little data.

- Underfitting (high bias)

    - Model is too simple to capture patterns.

    - Performs poorly on both training and unseen data.

    - Cause: model too shallow/simple, too strong regularization, not enough training.

🧪 How to Detect

- Overfitting:

    - Training accuracy ≫ Validation/Test accuracy.

    - Training loss keeps dropping, validation loss starts rising.

- Underfitting:

    - Both training and validation accuracy are low.

    - Loss is high and does not improve much during training.

🎤 Interview-style Answer (30s)

“Overfitting happens when a model memorizes training data, so it performs well on train but poorly on test. I’d detect it if training accuracy is high but validation accuracy drops, or validation loss rises while training loss falls. Underfitting is the opposite — the model is too simple, performs badly on both train and test. I’d detect it if accuracy is low across the board. To fix overfitting, I’d use regularization, dropout, or early stopping. To fix underfitting, I’d increase model complexity, add features, or train longer.”


### “How does backpropagation work in a neural network?”

🔎 Backpropagation in a Nutshell

Goal: Adjust weights so the network’s predictions get closer to the correct outputs.

Step-by-step

Forward pass

Input flows through the network (Input → Hidden Layers → Output).

Each neuron computes: weighted sum + bias → activation.

Output is produced.

Loss calculation

Compare prediction with the true label using a loss function (e.g., cross-entropy, MSE).

Backward pass (backpropagation)

Compute how much each weight contributed to the error.

Use the chain rule of calculus to propagate gradients backward layer by layer.

Each neuron gets a gradient telling it how to adjust.

Weight update (optimization)

Optimizer (SGD, Adam, RMSProp, etc.) updates weights:

    weight = weight - learning_rate * gradient

= gradient of loss wrt weight.

Repeat

Do this for many epochs until the network converges.

🎤 Interview-style Answer (30s)

“Backpropagation is the process of updating neural network weights using the chain rule of calculus. First, the network makes a forward pass and computes a loss. Then, gradients of the loss are propagated backward through the layers, showing how much each weight contributed to the error. Finally, an optimizer like SGD or Adam updates the weights in the direction that reduces the loss. This cycle repeats until the model converges.”

### “Why do we need activation functions in neural networks?”

1. Introduce Non-linearity

    - Without activation functions, a neural network is just a stack of linear transformations.

    - Multiple linear layers collapse into one → equivalent to linear regression.

    - With nonlinear activations (ReLU, sigmoid, tanh), the network can approximate nonlinear decision boundaries.

1. Allow Complex Representations

    - Nonlinear activations let the network capture patterns like curves, images, language, etc.

    - They allow hierarchical feature extraction: edges → shapes → objects → semantics.

1. Enable Universal Approximation

    - The Universal Approximation Theorem: a neural network with at least one hidden layer and nonlinear activation can approximate any continuous function.

#### 🛠️ Common Activation Functions

- Sigmoid (σ) – squashes values to [0, 1], used in binary classification.

- Tanh – squashes to [-1, 1], zero-centered.

- ReLU – Rectified Linear Unit, most popular in deep learning (simple & efficient).

- Softmax – converts outputs into probabilities for multi-class classification.

#### 🎤 Interview-style Answer (30s)

“We need activation functions to introduce nonlinearity. Without them, a neural network is just a linear model, no matter how many layers we stack. Activation functions like ReLU, sigmoid, and tanh allow the network to learn complex, nonlinear patterns and approximate any function. That’s what makes deep learning powerful.”

### “How would you prevent overfitting in a deep learning model?”

1. Regularization

- L1 (Lasso) → encourages sparsity.

- L2 (Ridge / weight decay) → keeps weights small.

- Prevents the model from fitting noise.

2. Dropout

- Randomly “turns off” neurons during training.

- Forces the network to not rely too much on specific connections.

- Typical rates: 0.2–0.5.

3. Early Stopping

- Monitor validation loss.

- Stop training when validation performance starts degrading.

4. Data Augmentation

- Especially for CV and NLP.

- Images: rotation, flipping, cropping, color jitter.

- Text: synonym replacement, back-translation.

- Makes the model generalize better.

5. Simpler Models

- Reduce network depth/width.

- Over-parameterized models tend to memorize.

6. More Data

- The most powerful fix.

- Collect more samples or generate synthetic ones (SMOTE, GANs).

7. Batch Normalization & Regular Training Tricks

- Normalizes activations → smoother training.

- Use proper learning rate schedules.

#### 🎤 Interview-style Answer (30s)

“Overfitting means the model memorizes training data instead of generalizing. I’d detect it when training accuracy is high but validation accuracy drops. To prevent it, I’d apply regularization (L1/L2), dropout, early stopping, and data augmentation. If possible, I’d also gather more data or simplify the model. In practice, I usually monitor validation curves and apply these techniques iteratively.”
