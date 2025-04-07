// to format time series data
export const preprocessTimeSeries = (rawData, maxTicks = 7) => {
    const dateToTotalMap = new Map();
    rawData.forEach(item => {
      dateToTotalMap.set(item.date, item.total);
    });
  
    const allDates = [];
    const startDate = new Date(rawData[0].date);
    const endDate = new Date(rawData[rawData.length - 1].date);
  
    for (
      let d = new Date(startDate);
      d <= endDate;
      d.setDate(d.getDate() + 1)
    ) {
      const iso = d.toISOString().split("T")[0]; // YYYY-MM-DD
      allDates.push(iso);
    }
  
    const filledData = allDates.map(date => ({
      x: new Date(date).toLocaleDateString(), // for display
      y: dateToTotalMap.get(date) ?? 0,
      rawDate: date,
    }));
  
    // Calculate 7 evenly spaced ticks
    const tickInterval = Math.max(1, Math.floor(filledData.length / maxTicks));
    const tickValues = filledData
      .filter((_, idx) => idx % tickInterval === 0)
      .map(d => d.x);
  
    return { filledData, tickValues };
  };