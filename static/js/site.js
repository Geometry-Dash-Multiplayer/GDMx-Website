// Function to generate a random number between a range
function getRandom(min, max) {
    return Math.random() * (max - min) + min;
}

// Recursive function to move a single bubble smoothly
function moveBubble(bubble) {
    const radius = parseFloat(bubble.getAttribute("r"));
    const moveRangeMin = 0.1 * radius;
    const moveRangeMax = 0.5 * radius;

    const currentTransform = bubble.getAttribute('transform') || "";
    const matches = currentTransform.match(/translate\(([\d\.\-]+),\s*([\d\.\-]+)\)/);
    const currentX = matches ? parseFloat(matches[1]) : 0;
    const currentY = matches ? parseFloat(matches[2]) : 0;

    const tx = currentX + getRandom(-moveRangeMax, moveRangeMax);
    const ty = currentY + getRandom(-moveRangeMax, moveRangeMax);
    const duration = getRandom(2000, 5000);

    let startTime = null;

    function animateBubble(time) {
        if (!startTime) startTime = time;
        const elapsedTime = time - startTime;
        const progress = elapsedTime / duration;

        const currentTx = currentX + (tx - currentX) * progress;
        const currentTy = currentY + (ty - currentY) * progress;

        bubble.setAttribute('transform', `translate(${currentTx}, ${currentTy})`);

        if (elapsedTime < duration) {
            requestAnimationFrame(animateBubble);
        } else {
            moveBubble(bubble);
        }
    }
    requestAnimationFrame(animateBubble);
}

function startBubblesMovement() {
    const bubbles = document.querySelectorAll('circle');
    bubbles.forEach(bubble => {
        moveBubble(bubble);
    });
}
document.addEventListener('DOMContentLoaded', startBubblesMovement);
