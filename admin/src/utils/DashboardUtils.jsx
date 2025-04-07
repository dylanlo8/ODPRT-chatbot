// Downsampling algorithm for LineChart
export const downsample = (data, maxPoints) => {
  const total = data.length;
  if (total <= maxPoints) return data;

  const step = Math.floor(total / maxPoints);
  const sampled = [];

  for (let i = 0; i < total && sampled.length < maxPoints; i += step) {
    sampled.push(data[i]);
  }

  // Ensure the last point is included
  if (sampled[sampled.length - 1] !== data[total - 1]) {
    sampled[sampled.length - 1] = data[total - 1];
  }

  return sampled;
};