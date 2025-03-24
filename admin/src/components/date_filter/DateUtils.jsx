// dateUtils.js
export const filterDataByDate = (data, dateRange) => {
    if (!dateRange.from || !dateRange.to) return data;
  
    const fromDate = new Date(dateRange.from);
    const toDate = new Date(dateRange.to);
  
    return data.filter((item) => {
      const itemDate = new Date(item.date);
      return itemDate >= fromDate && itemDate <= toDate;
    });
  };
  