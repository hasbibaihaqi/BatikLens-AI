/* ============================================================
   BATIKLENS — main.js
   UI interactions, drag & drop, animations
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {

    // =============================================
    //  AOS (Animate On Scroll) Init
    // =============================================
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 700,
            easing: "ease-out-cubic",
            once: true,
            offset: 50
        });
    }

    // =============================================
    //  Navbar scroll effect
    // =============================================
    var navbar = document.getElementById("mainNavbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 30) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        }, { passive: true });
    }

    // =============================================
    //  Upload / Drag & Drop Logic
    // =============================================
    var fileInput      = document.getElementById("file-input");
    var dropZone       = document.getElementById("upload-drop-zone");
    var previewCont    = document.getElementById("image-preview-container");
    var previewImg     = document.getElementById("image-preview");
    var previewName    = document.getElementById("preview-filename");
    var removeBtn      = document.getElementById("remove-preview-btn");
    var uploadForm     = document.getElementById("upload-form");
    var btnPredict     = document.getElementById("btn-predict");
    var btnText        = document.getElementById("btn-text");
    var btnSpinner     = document.getElementById("btn-spinner");
    var loadingOverlay = document.getElementById("loading-overlay");

    // Allowed image types (client-side check)
    var ALLOWED_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif", "image/bmp"];
    var MAX_SIZE_MB   = 5;

    /** Show image preview */
    function showPreview(file) {
        if (!file) return;

        // Type check
        if (!ALLOWED_TYPES.includes(file.type)) {
            showToast("Format file tidak didukung. Gunakan PNG, JPG, JPEG, atau WEBP.", "danger");
            return;
        }

        // Size check
        if (file.size > MAX_SIZE_MB * 1024 * 1024) {
            showToast("Ukuran file terlalu besar. Maksimal " + MAX_SIZE_MB + "MB.", "danger");
            return;
        }

        var reader = new FileReader();
        reader.onload = function (e) {
            if (previewImg)  previewImg.src = e.target.result;
            if (previewCont) previewCont.classList.remove("d-none");
            if (previewName) previewName.textContent = file.name + " (" + (file.size / 1024).toFixed(1) + " KB)";
            if (btnPredict)  btnPredict.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    /** Clear preview and reset form state */
    function clearPreview() {
        if (previewImg)  previewImg.src = "";
        if (previewCont) previewCont.classList.add("d-none");
        if (previewName) previewName.textContent = "";
        if (fileInput)   fileInput.value = "";
        if (btnPredict)  btnPredict.disabled = true;
    }

    /** Assign file to input via DataTransfer */
    function assignFileToInput(file) {
        try {
            var dt = new DataTransfer();
            dt.items.add(file);
            if (fileInput) fileInput.files = dt.files;
        } catch (err) {
            // DataTransfer not supported (old browsers) — skip
        }
    }

    // ——— File Input Change ———
    if (fileInput) {
        fileInput.addEventListener("change", function () {
            var file = this.files && this.files[0];
            if (file) showPreview(file);
        });
    }

    // ——— Remove Preview ———
    if (removeBtn) {
        removeBtn.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            clearPreview();
        });
    }

    // ——— Keyboard activation of drop zone ———
    if (dropZone) {
        dropZone.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                if (fileInput) fileInput.click();
            }
        });
    }

    // ——— Drag & Drop ———
    if (dropZone) {

        // Prevent browser default drag behaviors on the whole window
        ["dragenter", "dragover", "dragleave", "drop"].forEach(function (evtName) {
            document.body.addEventListener(evtName, function (e) { e.preventDefault(); }, false);
        });

        dropZone.addEventListener("dragenter", function (e) {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });

        dropZone.addEventListener("dragover", function (e) {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });

        dropZone.addEventListener("dragleave", function (e) {
            // Only remove class if leaving the drop zone entirely
            if (!dropZone.contains(e.relatedTarget)) {
                dropZone.classList.remove("drag-over");
            }
        });

        dropZone.addEventListener("drop", function (e) {
            e.preventDefault();
            dropZone.classList.remove("drag-over");

            var files = e.dataTransfer && e.dataTransfer.files;
            if (files && files.length > 0) {
                var file = files[0];
                assignFileToInput(file);
                showPreview(file);
            }
        });
    }

    // ——— Form Submit ———
    if (uploadForm) {
        uploadForm.addEventListener("submit", function (e) {
            var hasFile = fileInput && fileInput.files && fileInput.files.length > 0;
            if (!hasFile) {
                e.preventDefault();
                showToast("Silakan pilih gambar batik terlebih dahulu.", "warning");
                return;
            }

            // Show loading overlay
            if (loadingOverlay) loadingOverlay.classList.add("active");

            // Update button state
            if (btnText)    btnText.classList.add("d-none");
            if (btnSpinner) btnSpinner.classList.remove("d-none");
            if (btnPredict) btnPredict.disabled = true;
        });
    }

    // =============================================
    //  Confidence Bar Animation (result page)
    // =============================================
    var bars = document.querySelectorAll(".confidence-fill");
    bars.forEach(function (bar) {
        var target = parseFloat(bar.getAttribute("data-target") || "0");
        // Use requestAnimationFrame + small timeout for CSS transition
        setTimeout(function () {
            bar.style.width = target + "%";
        }, 400);
    });

    // =============================================
    //  Simple Toast Notification
    // =============================================
    function showToast(message, type) {
        type = type || "info";
        var colors = {
            danger:  { bg: "rgba(239,68,68,0.12)",  border: "rgba(239,68,68,0.4)",  icon: "fa-circle-exclamation" },
            warning: { bg: "rgba(245,158,11,0.12)", border: "rgba(245,158,11,0.4)", icon: "fa-triangle-exclamation" },
            success: { bg: "rgba(16,185,129,0.12)", border: "rgba(16,185,129,0.4)", icon: "fa-circle-check" },
            info:    { bg: "rgba(99,102,241,0.12)", border: "rgba(99,102,241,0.4)", icon: "fa-circle-info" }
        };
        var c = colors[type] || colors.info;

        var toast = document.createElement("div");
        toast.style.cssText = [
            "position:fixed",
            "bottom:24px",
            "right:24px",
            "z-index:9999",
            "background:" + c.bg,
            "border:1px solid " + c.border,
            "backdrop-filter:blur(16px)",
            "-webkit-backdrop-filter:blur(16px)",
            "color:#fff",
            "padding:14px 20px",
            "border-radius:12px",
            "font-size:0.875rem",
            "font-family:var(--font-sans,Inter,sans-serif)",
            "max-width:340px",
            "display:flex",
            "align-items:center",
            "gap:10px",
            "box-shadow:0 10px 40px rgba(0,0,0,0.4)",
            "transform:translateY(80px)",
            "opacity:0",
            "transition:all 0.35s cubic-bezier(0.4,0,0.2,1)"
        ].join(";");

        toast.innerHTML = '<i class="fa-solid ' + c.icon + '"></i><span>' + message + "</span>";
        document.body.appendChild(toast);

        // Animate in
        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                toast.style.transform = "translateY(0)";
                toast.style.opacity = "1";
            });
        });

        // Auto remove after 4s
        setTimeout(function () {
            toast.style.transform = "translateY(80px)";
            toast.style.opacity = "0";
            setTimeout(function () {
                if (toast.parentNode) toast.parentNode.removeChild(toast);
            }, 350);
        }, 4000);
    }

    // =============================================
    //  About Page: motif card hover glow
    // =============================================
    var motifCards = document.querySelectorAll(".motif-catalog-card");
    motifCards.forEach(function (card) {
        card.addEventListener("keydown", function (e) {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                card.click();
            }
        });
    });

    // =============================================
    //  Smooth scroll for hero scroll hint
    // =============================================
    var scrollHint = document.querySelector(".scroll-hint");
    if (scrollHint) {
        scrollHint.style.cursor = "pointer";
        scrollHint.addEventListener("click", function () {
            var features = document.getElementById("features");
            if (features) features.scrollIntoView({ behavior: "smooth" });
        });
    }

});