## Exercise 3: Edge ML Optimization (90 minutes)

**Objective**: Optimize ML models for edge deployment with quantization, pruning, and compilation techniques.

### Background

Edge ML requires:
- Model compression (quantization, pruning)
- Hardware-specific optimization
- Latency and memory constraints
- Battery efficiency considerations

### Tasks

1. **Implement quantization**:
   - Post-training quantization (PTQ)
   - Quantization-aware training (QAT)
   - Compare INT8 and FP16 performance
   - Measure accuracy degradation

2. **Apply model pruning**:
   - Structured pruning
   - Unstructured pruning
   - Gradual magnitude pruning
   - Fine-tuning after pruning

3. **Optimize for target hardware**:
   - Convert to TensorFlow Lite
   - Convert to ONNX Runtime
   - Optimize for specific hardware
   - Benchmark on target device

4. **Implement inference pipeline**:
   - Preprocessing optimization
   - Batch processing
   - Model caching
   - Power-aware scheduling

### Starter Code

```python
# edge_ml_optimization.py
"""
Edge ML model optimization with quantization and pruning.
"""

import tensorflow as tf
import tensorflow_model_optimization as tfmot
import numpy as np
from typing import Tuple, Optional, Dict
import logging
import time
from pathlib import Path

class ModelQuantizer:
    """
    Quantize models for edge deployment.

    TODO: Implement quantization techniques
    """

    def __init__(self, model: tf.keras.Model):
        """Initialize quantizer with model."""
        self.model = model
        self.quantized_model = None

    def post_training_quantization(
        self,
        representative_dataset: np.ndarray,
        quantization_type: str = "int8"  # "int8", "float16", "dynamic"
    ) -> tf.lite.TFLiteConverter:
        """
        Apply post-training quantization.

        TODO: Implement PTQ
        - Convert to TFLite
        - Apply quantization
        - Set optimization flags
        """
        # TODO: Create TFLite converter
        # converter = tf.lite.TFLiteConverter.from_keras_model(self.model)

        # TODO: Set optimization
        # if quantization_type == "int8":
        #     converter.optimizations = [tf.lite.Optimize.DEFAULT]
        #
        #     # Representative dataset for calibration
        #     def representative_dataset_gen():
        #         for sample in representative_dataset:
        #             yield [sample.astype(np.float32)]
        #
        #     converter.representative_dataset = representative_dataset_gen
        #     converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        #     converter.inference_input_type = tf.int8
        #     converter.inference_output_type = tf.int8

        # elif quantization_type == "float16":
        #     converter.optimizations = [tf.lite.Optimize.DEFAULT]
        #     converter.target_spec.supported_types = [tf.float16]

        # elif quantization_type == "dynamic":
        #     converter.optimizations = [tf.lite.Optimize.DEFAULT]

        # TODO: Convert model
        # self.quantized_model = converter.convert()

        # return converter

        pass

    def quantization_aware_training(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        val_data: Tuple[np.ndarray, np.ndarray],
        epochs: int = 10
    ) -> tf.keras.Model:
        """
        Apply quantization-aware training.

        TODO: Implement QAT
        - Add quantization layers
        - Train with quantization simulation
        - Fine-tune model
        """
        # TODO: Create QAT model
        # quantize_model = tfmot.quantization.keras.quantize_model
        # qat_model = quantize_model(self.model)

        # TODO: Compile model
        # qat_model.compile(
        #     optimizer='adam',
        #     loss='sparse_categorical_crossentropy',
        #     metrics=['accuracy']
        # )

        # TODO: Train
        # history = qat_model.fit(
        #     train_data[0], train_data[1],
        #     batch_size=32,
        #     epochs=epochs,
        #     validation_data=val_data
        # )

        # TODO: Convert to TFLite
        # converter = tf.lite.TFLiteConverter.from_keras_model(qat_model)
        # converter.optimizations = [tf.lite.Optimize.DEFAULT]
        # self.quantized_model = converter.convert()

        # return qat_model

        pass

    def save_quantized_model(self, output_path: str):
        """
        Save quantized model.

        TODO: Save TFLite model
        """
        if self.quantized_model is None:
            raise ValueError("No quantized model available. Run quantization first.")

        # TODO: Save model
        # with open(output_path, 'wb') as f:
        #     f.write(self.quantized_model)

        # logging.info(f"Quantized model saved to {output_path}")

        pass

    def benchmark_quantized_model(
        self,
        test_data: np.ndarray,
        num_runs: int = 100
    ) -> Dict:
        """
        Benchmark quantized model performance.

        TODO: Measure latency and accuracy
        """
        if self.quantized_model is None:
            raise ValueError("No quantized model available")

        # TODO: Create interpreter
        # interpreter = tf.lite.Interpreter(model_content=self.quantized_model)
        # interpreter.allocate_tensors()

        # TODO: Get input/output details
        # input_details = interpreter.get_input_details()
        # output_details = interpreter.get_output_details()

        # TODO: Benchmark inference
        # latencies = []
        # for _ in range(num_runs):
        #     sample = test_data[np.random.randint(len(test_data))]
        #
        #     start = time.time()
        #     interpreter.set_tensor(input_details[0]['index'], sample[np.newaxis, ...])
        #     interpreter.invoke()
        #     output = interpreter.get_tensor(output_details[0]['index'])
        #     latency = time.time() - start
        #
        #     latencies.append(latency)

        # TODO: Calculate statistics
        # return {
        #     'avg_latency_ms': np.mean(latencies) * 1000,
        #     'p50_latency_ms': np.percentile(latencies, 50) * 1000,
        #     'p95_latency_ms': np.percentile(latencies, 95) * 1000,
        #     'p99_latency_ms': np.percentile(latencies, 99) * 1000,
        #     'throughput_qps': 1.0 / np.mean(latencies)
        # }

        pass


class ModelPruner:
    """
    Prune models for efficiency.

    TODO: Implement pruning techniques
    """

    def __init__(self, model: tf.keras.Model):
        """Initialize pruner with model."""
        self.model = model
        self.pruned_model = None

    def magnitude_pruning(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        target_sparsity: float = 0.5,
        epochs: int = 10
    ) -> tf.keras.Model:
        """
        Apply magnitude-based pruning.

        TODO: Implement magnitude pruning
        - Define pruning schedule
        - Apply pruning to layers
        - Fine-tune pruned model
        """
        # TODO: Define pruning schedule
        # prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude

        # pruning_params = {
        #     'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
        #         initial_sparsity=0.0,
        #         final_sparsity=target_sparsity,
        #         begin_step=0,
        #         end_step=epochs * len(train_data[0]) // 32
        #     )
        # }

        # TODO: Apply pruning to model
        # self.pruned_model = prune_low_magnitude(self.model, **pruning_params)

        # TODO: Compile and train
        # self.pruned_model.compile(
        #     optimizer='adam',
        #     loss='sparse_categorical_crossentropy',
        #     metrics=['accuracy']
        # )

        # callbacks = [
        #     tfmot.sparsity.keras.UpdatePruningStep(),
        #     tfmot.sparsity.keras.PruningSummaries(log_dir='./logs')
        # ]

        # self.pruned_model.fit(
        #     train_data[0], train_data[1],
        #     batch_size=32,
        #     epochs=epochs,
        #     callbacks=callbacks
        # )

        # TODO: Strip pruning wrappers
        # self.pruned_model = tfmot.sparsity.keras.strip_pruning(self.pruned_model)

        # return self.pruned_model

        pass

    def structured_pruning(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        pruning_ratio: float = 0.3
    ):
        """
        Apply structured pruning (remove entire channels/filters).

        TODO: Implement structured pruning
        """
        # TODO: Analyze layer importance
        # TODO: Remove least important channels
        # TODO: Fine-tune reduced model
        pass

    def measure_sparsity(self) -> float:
        """
        Measure model sparsity.

        TODO: Calculate percentage of zero weights
        """
        if self.pruned_model is None:
            model_to_check = self.model
        else:
            model_to_check = self.pruned_model

        # TODO: Count zero weights
        # total_weights = 0
        # zero_weights = 0

        # for layer in model_to_check.layers:
        #     if hasattr(layer, 'kernel'):
        #         weights = layer.kernel.numpy()
        #         total_weights += weights.size
        #         zero_weights += np.sum(weights == 0)

        # sparsity = zero_weights / total_weights
        # return sparsity

        pass


class EdgeMLPipeline:
    """
    Complete edge ML optimization pipeline.

    TODO: Implement end-to-end optimization
    """

    def __init__(self, model: tf.keras.Model):
        """Initialize pipeline."""
        self.original_model = model
        self.optimized_model = None
        self.quantizer = ModelQuantizer(model)
        self.pruner = ModelPruner(model)

    def optimize(
        self,
        train_data: Tuple[np.ndarray, np.ndarray],
        val_data: Tuple[np.ndarray, np.ndarray],
        test_data: np.ndarray,
        target_size_mb: float = 10.0,
        target_latency_ms: float = 100.0
    ) -> Dict:
        """
        Optimize model to meet constraints.

        TODO: Implement optimization pipeline
        - Apply pruning
        - Apply quantization
        - Measure metrics
        - Iterate if needed
        """
        logging.info("Starting edge ML optimization pipeline")

        # TODO: 1. Baseline metrics
        # baseline_metrics = self._evaluate_model(self.original_model, val_data)
        # logging.info(f"Baseline accuracy: {baseline_metrics['accuracy']:.4f}")

        # TODO: 2. Apply pruning
        # logging.info("Applying pruning...")
        # pruned_model = self.pruner.magnitude_pruning(
        #     train_data,
        #     target_sparsity=0.5,
        #     epochs=5
        # )

        # TODO: 3. Apply quantization
        # logging.info("Applying quantization...")
        # self.quantizer.model = pruned_model
        # self.quantizer.post_training_quantization(
        #     train_data[0][:100],
        #     quantization_type="int8"
        # )

        # TODO: 4. Benchmark optimized model
        # optimized_metrics = self.quantizer.benchmark_quantized_model(
        #     test_data,
        #     num_runs=100
        # )

        # TODO: 5. Calculate compression ratio
        # original_size = self._get_model_size(self.original_model)
        # optimized_size = len(self.quantizer.quantized_model) / (1024 * 1024)
        # compression_ratio = original_size / optimized_size

        # TODO: Return results
        # return {
        #     'baseline_accuracy': baseline_metrics['accuracy'],
        #     'optimized_latency_ms': optimized_metrics['avg_latency_ms'],
        #     'original_size_mb': original_size,
        #     'optimized_size_mb': optimized_size,
        #     'compression_ratio': compression_ratio,
        #     'meets_constraints': (
        #         optimized_size <= target_size_mb and
        #         optimized_metrics['avg_latency_ms'] <= target_latency_ms
        #     )
        # }

        pass

    def _evaluate_model(self, model: tf.keras.Model, data: Tuple) -> Dict:
        """Evaluate model accuracy."""
        # loss, accuracy = model.evaluate(data[0], data[1], verbose=0)
        # return {'loss': loss, 'accuracy': accuracy}
        pass

    def _get_model_size(self, model: tf.keras.Model) -> float:
        """Get model size in MB."""
        # temp_path = '/tmp/temp_model.h5'
        # model.save(temp_path)
        # size_mb = Path(temp_path).stat().st_size / (1024 * 1024)
        # Path(temp_path).unlink()
        # return size_mb
        pass


# Example usage
if __name__ == "__main__":
    # TODO: Create sample model
    # model = tf.keras.Sequential([
    #     tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    #     tf.keras.layers.MaxPooling2D(),
    #     tf.keras.layers.Conv2D(64, 3, activation='relu'),
    #     tf.keras.layers.MaxPooling2D(),
    #     tf.keras.layers.Flatten(),
    #     tf.keras.layers.Dense(128, activation='relu'),
    #     tf.keras.layers.Dense(10, activation='softmax')
    # ])

    # TODO: Load data (e.g., MNIST)
    # (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    # x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255
    # x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255

    # TODO: Train baseline model
    # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    # model.fit(x_train, y_train, epochs=5, validation_split=0.2)

    # TODO: Optimize for edge
    # pipeline = EdgeMLPipeline(model)
    # results = pipeline.optimize(
    #     train_data=(x_train, y_train),
    #     val_data=(x_test, y_test),
    #     test_data=x_test,
    #     target_size_mb=5.0,
    #     target_latency_ms=50.0
    # )

    # print(results)

    pass
```

### Success Criteria

- [ ] Model size reduced by >4x through quantization
- [ ] Pruning achieves >50% sparsity
- [ ] Accuracy degradation < 2% from baseline
- [ ] Inference latency meets target
- [ ] TFLite model runs on mobile/edge device
- [ ] Power consumption measured and optimized

### Solution Hints

<details>
<summary>Click to reveal hints</summary>

1. **Quantization**: Start with dynamic quantization, then PTQ, then QAT if needed
2. **Pruning**: Apply gradual magnitude pruning during fine-tuning
3. **Evaluation**: Test on actual target hardware, simulators can be misleading
4. **Accuracy**: Monitor accuracy at each optimization step
5. **Combined**: Prune first, then quantize for best results
6. **Hardware**: Use TFLite delegates for GPU/NPU acceleration

</details>

---
