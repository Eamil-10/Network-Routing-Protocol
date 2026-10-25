/**
 * Simulation Engine for BFS and DFS Graph Traversals
 * Coordinates interactive step-by-step playback, queue/stack visualization,
 * parent reconstruction, and educational explanations.
 */

class TraversalSimulation {
  constructor(cyView, uiContainers) {
    this.cyView = cyView;
    this.ui = uiContainers; // references to DOM elements

    this.steps = [];
    this.currentIndex = -1;
    this.isPlaying = false;
    this.speedMs = 800;
    this.timer = null;
    this.currentAlgorithm = "BFS";
    this.finalResult = null;
  }

  loadSimulation(result, algorithm = "BFS") {
    this.reset();
    this.finalResult = result;
    this.currentAlgorithm = algorithm;
    this.steps = result.steps || [];
    this.currentIndex = -1;

    // Reset UI
    this.cyView.resetSimulationVisuals();
    this.updateControlsState();
    this.renderInitialUI();

    if (this.steps.length > 0) {
      this.stepForward();
    }
  }

  setSpeed(speedMs) {
    this.speedMs = parseInt(speedMs, 10);
  }

  start() {
    if (this.steps.length === 0) return;
    this.isPlaying = true;
    this.updateControlsState();
    this.playLoop();
  }

  playLoop() {
    if (!this.isPlaying) return;

    if (this.currentIndex < this.steps.length - 1) {
      this.stepForward();
      this.timer = setTimeout(() => this.playLoop(), this.speedMs);
    } else {
      this.pause();
    }
  }

  pause() {
    this.isPlaying = false;
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }
    this.updateControlsState();
  }

  resume() {
    if (this.currentIndex >= this.steps.length - 1) {
      this.currentIndex = -1;
      this.cyView.resetSimulationVisuals();
    }
    this.start();
  }

  reset() {
    this.pause();
    this.currentIndex = -1;
    this.steps = [];
    this.finalResult = null;
    this.cyView.resetSimulationVisuals();
    this.clearUI();
    this.updateControlsState();
  }

  stepForward() {
    if (this.currentIndex < this.steps.length - 1) {
      this.currentIndex++;
      this.applyStep(this.steps[this.currentIndex]);
      this.updateControlsState();
    } else {
      this.pause();
    }
  }

  stepBackward() {
    if (this.currentIndex > 0) {
      this.pause();
      this.currentIndex--;
      // Re-apply up to currentIndex
      this.cyView.resetSimulationVisuals();
      for (let i = 0; i <= this.currentIndex; i++) {
        this.applyStep(this.steps[i], i === this.currentIndex);
      }
      this.updateControlsState();
    } else if (this.currentIndex === 0) {
      this.pause();
      this.currentIndex = -1;
      this.cyView.resetSimulationVisuals();
      this.clearUI();
      this.renderInitialUI();
      this.updateControlsState();
    }
  }

  applyStep(step, isCurrentActive = true) {
    if (!step) return;

    // 1. Update Cytoscape Graph
    if (step.action === "INITIALIZE") {
      this.cyView.resetSimulationVisuals();
      if (this.currentAlgorithm === "BFS") {
        this.cyView.highlightQueuedNode(step.current_node);
      } else {
        this.cyView.highlightCurrentNode(step.current_node);
      }
    } else if (step.action === "DEQUEUE" || step.action === "POP_VISIT") {
      this.cyView.highlightCurrentNode(step.current_node);
    } else if (step.action === "ENQUEUE_NEIGHBOR") {
      this.cyView.highlightQueuedNode(step.neighbor);
      this.cyView.highlightEdgeTraversed(step.current_node, step.neighbor);
    } else if (step.action === "PUSH_NEIGHBOR") {
      this.cyView.highlightQueuedNode(step.neighbor);
      this.cyView.highlightEdgeTraversed(step.current_node, step.neighbor);
    } else if (step.action === "PATH_RECONSTRUCTED") {
      this.cyView.highlightFinalPath(step.final_path);
    } else if (step.action === "DEAD_END_BACKTRACK") {
      this.cyView.highlightVisitedNode(step.current_node);
    }

    if (step.visited) {
      step.visited.forEach((v) => {
        if (v !== step.current_node) {
          this.cyView.highlightVisitedNode(v);
        }
      });
    }

    // 2. Update Queue or Stack Container
    if (this.currentAlgorithm === "BFS") {
      this.renderQueueView(step.queue || []);
    } else {
      this.renderStackView(step.stack || [], step.is_backtracking);
    }

    // 3. Update Visited Display
    if (this.ui.visitedBox) {
      this.ui.visitedBox.innerHTML =
        step.visited && step.visited.length > 0
          ? step.visited
              .map(
                (n) =>
                  `<span class="badge ${
                    n === step.current_node ? "badge-warning" : "badge-info"
                  }">${n}</span>`
              )
              .join(" ")
          : '<span class="text-muted">None</span>';
    }

    // 4. Update Parent Map
    this.renderParentMap(step.parent_map || {});

    // 5. Update Current Node and Metrics
    if (this.ui.currentNodeBadge) {
      this.ui.currentNodeBadge.textContent = step.current_node || "None";
    }
    if (this.ui.stepCounterBadge) {
      this.ui.stepCounterBadge.textContent = `${this.currentIndex + 1} / ${this.steps.length}`;
    }

    // 6. Update Educational Explanation (single sentence for unified box or full banner)
    if (this.ui.explanationText) {
      this.ui.explanationText.textContent = step.message || "Traversing graph...";
    }
    if (this.ui.explanationBox) {
      this.ui.explanationBox.innerHTML = `
        <div class="educational-banner">
          <h4>${step.action.replace(/_/g, " ")}</h4>
          <p>${step.message}</p>
        </div>
      `;
    }

    // 7. Append Step Log (only if current active step)
    if (isCurrentActive) {
      this.appendStepLog(step);
      if (this.onStepChange) {
        this.onStepChange(step, this.currentIndex, this.steps.length);
      }
    }

    // 8. If destination reached or final path reconstructed, show reconstruction
    if (step.action === "PATH_RECONSTRUCTED" && this.finalResult) {
      this.renderReconstructionTrace(this.finalResult.reconstruction_steps, this.finalResult.route);
      if (this.ui.finalRouteBox && this.ui.finalRoutePath) {
        this.ui.finalRouteBox.style.display = "block";
        this.ui.finalRoutePath.textContent = this.finalResult.route ? this.finalResult.route.join(" → ") : "None";
      }
    }
  }

  renderQueueView(queueItems) {
    if (this.ui.dsTitle) this.ui.dsTitle.textContent = "📦 Live FIFO Queue (Front ➔ Rear)";
    if (this.ui.dsSize) this.ui.dsSize.textContent = `${queueItems.length} item${queueItems.length === 1 ? "" : "s"}`;
    if (this.ui.backtrackBadge) this.ui.backtrackBadge.style.display = "none";
    if (!this.ui.dsContainer) return;

    if (queueItems.length === 0) {
      this.ui.dsContainer.innerHTML = `
        <div class="queue-strip">
          <span class="text-muted" style="font-size: 0.8rem;">Queue is empty</span>
        </div>`;
      return;
    }

    let html = `
      <div class="queue-strip">
        <span class="queue-tag tag-front">FRONT</span>`;
    queueItems.forEach((item, idx) => {
      html += `<div class="queue-item">${item}</div>`;
      if (idx < queueItems.length - 1) {
        html += `<span style="color: #94a3b8; font-weight: bold;">→</span>`;
      }
    });
    html += `<span class="queue-tag tag-rear">REAR</span></div>`;
    this.ui.dsContainer.innerHTML = html;
  }

  renderStackView(stackItems, isBacktracking = false) {
    if (this.ui.dsTitle) this.ui.dsTitle.textContent = "📚 Live LIFO Stack (Bottom ➔ Top)";
    if (this.ui.dsSize) this.ui.dsSize.textContent = `${stackItems.length} item${stackItems.length === 1 ? "" : "s"}`;
    if (this.ui.backtrackBadge) {
      this.ui.backtrackBadge.style.display = isBacktracking ? "inline-block" : "none";
    }
    if (!this.ui.dsContainer) return;

    if (stackItems.length === 0) {
      this.ui.dsContainer.innerHTML = `
        <div class="stack-column" style="justify-content: center; align-items: center; min-height: 40px;">
          <span class="text-muted" style="font-size: 0.8rem;">Stack is empty</span>
        </div>`;
      return;
    }

    let html = "";
    if (isBacktracking) {
      html += `
        <div class="alert-box alert-warning" style="padding: 4px 8px; margin-bottom: 6px; font-size: 0.75rem;">
          ⚠️ <strong>Dead End!</strong> Backtracking up stack.
        </div>`;
    }

    html += `<div class="stack-column">`;
    // Stack is rendered vertically. Last element in array is TOP of stack.
    stackItems.forEach((item, idx) => {
      const isTop = idx === stackItems.length - 1;
      html += `
        <div class="stack-item ${isTop ? "top-item" : ""}">
          ${item} ${isTop ? '<span class="badge badge-warning" style="margin-left: 4px; font-size: 0.65rem;">TOP</span>' : ""}
        </div>`;
    });
    html += `</div>`;
    this.ui.dsContainer.innerHTML = html;
  }

  renderParentMap(parentMap) {
    if (!this.ui.parentTable) return;
    const entries = Object.entries(parentMap);
    if (entries.length === 0) {
      this.ui.parentTable.innerHTML = `<tr><td colspan="2" class="text-muted" style="text-align: center;">No parent mappings yet</td></tr>`;
      return;
    }

    let html = "";
    entries.forEach(([child, parent]) => {
      html += `
        <tr>
          <td><strong>${child}</strong></td>
          <td>${parent ? `<span class="badge badge-info">${parent}</span>` : '<span class="badge badge-success">SOURCE</span>'}</td>
        </tr>`;
    });
    this.ui.parentTable.innerHTML = html;
  }

  renderReconstructionTrace(reconstructionSteps, route) {
    if (!this.ui.reconstructionBox || !reconstructionSteps) return;

    let html = `
      <div class="card" style="margin-top: 14px; border-color: #10b981;">
        <div class="card-header" style="background: #ecfdf5;">
          <div class="card-title" style="color: #065f46;">
            ✅ Path Reconstruction via Parent Pointers
          </div>
        </div>
        <div class="card-body" style="font-size: 0.82rem;">
          <p style="margin-bottom: 8px; color: var(--text-muted);">
            Path reconstructed backwards from destination using <code>parent[node]</code>, then reversed:
          </p>
          <div class="linked-list-strip" style="background: #ffffff; border: 1px solid #a7f3d0;">
    `;

    reconstructionSteps.forEach((s, idx) => {
      html += `
        <div class="ll-node">
          <span class="ll-node-num">Step ${s.step}</span>
          <span class="ll-node-val">${s.node}</span>
          <span style="font-size: 0.65rem; color: #64748b;">parent: ${s.parent || "None"}</span>
        </div>
      `;
      if (idx < reconstructionSteps.length - 1) {
        html += `<span class="ll-arrow">←</span>`;
      }
    });

    html += `
          </div>
          <div style="margin-top: 10px; font-weight: 600; color: #047857;">
            Final Forward Route: ${route.join(" → ")} (${route.length - 1} hops)
          </div>
        </div>
      </div>
    `;
    this.ui.reconstructionBox.innerHTML = html;
  }

  appendStepLog(step) {
    if (!this.ui.stepLogContainer) return;
    const div = document.createElement("div");
    div.className = "step-log-item current-step";
    div.innerHTML = `
      <span class="step-num-badge">#${step.step}</span>
      <div>
        <strong>${step.action}</strong>: ${step.message}
      </div>
    `;

    // Remove current-step class from previous items
    const prevItems = this.ui.stepLogContainer.querySelectorAll(".step-log-item");
    prevItems.forEach((item) => item.classList.remove("current-step"));

    this.ui.stepLogContainer.appendChild(div);
    this.ui.stepLogContainer.scrollTop = this.ui.stepLogContainer.scrollHeight;
  }

  clearUI() {
    if (this.ui.dsContainer) this.ui.dsContainer.innerHTML = '<span class="text-muted" style="font-size: 0.8rem; margin: auto;">Empty</span>';
    if (this.ui.visitedBox) this.ui.visitedBox.innerHTML = '<span class="text-muted" style="font-size: 0.8rem;">None visited yet</span>';
    if (this.ui.parentTable) this.ui.parentTable.innerHTML = '<tr><td colspan="2" class="text-muted" style="text-align: center;">No parent mappings yet</td></tr>';
    if (this.ui.explanationText) this.ui.explanationText.textContent = 'Select endpoints and click "Run Traversal Calculation" to explore step-by-step.';
    if (this.ui.explanationBox) this.ui.explanationBox.innerHTML = "";
    if (this.ui.stepLogContainer) this.ui.stepLogContainer.innerHTML = "";
    if (this.ui.reconstructionBox) this.ui.reconstructionBox.innerHTML = "";
    if (this.ui.currentNodeBadge) this.ui.currentNodeBadge.textContent = "None";
    if (this.ui.stepCounterBadge) this.ui.stepCounterBadge.textContent = "0 / 0";
    if (this.ui.backtrackBadge) this.ui.backtrackBadge.style.display = "none";
    if (this.ui.finalRouteBox) this.ui.finalRouteBox.style.display = "none";
  }

  renderInitialUI() {
    this.clearUI();
    if (this.ui.stepLogContainer) {
      this.ui.stepLogContainer.innerHTML = `
        <div class="step-log-item">
          <span class="step-num-badge">INFO</span>
          <div>Simulation initialized. Click <strong>Start</strong> or <strong>Next Step</strong> to begin traversal.</div>
        </div>`;
    }
  }

  updateControlsState() {
    if (this.ui.btnStart) this.ui.btnStart.disabled = this.isPlaying || this.steps.length === 0;
    if (this.ui.btnPause) this.ui.btnPause.disabled = !this.isPlaying;
    if (this.ui.btnStep) this.ui.btnStep.disabled = this.isPlaying || this.currentIndex >= this.steps.length - 1;
    if (this.ui.btnPrev) this.ui.btnPrev.disabled = this.isPlaying || this.currentIndex < 0;
  }
}
