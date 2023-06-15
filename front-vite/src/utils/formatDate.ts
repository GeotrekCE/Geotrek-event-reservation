/**
 * Formate une date en format français DD/MM/YYYY
 * 
 * @param date Date à transformer de type YYYY-MM-DD
 */
export function formatDate(date?: string): string {
  if (!date) return '';
  const [year, month, day] = date.split('-');
  return `${day}/${month}/${year}`;
}

export function formatDateTime(date?: string): string {
  if (!date) return '';
  const [year, month, day] = date.substring(0, 10).split('-');
  return `${day}/${month}/${year}`;
}