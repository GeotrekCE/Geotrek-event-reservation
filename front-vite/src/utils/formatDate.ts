/**
 * Formate une date en format français DD/MM/YYYY
 * 
 * @param date Date à transformer de type YYYY-MM-DD
 */
export function formatDateString(date?: string): string {
  if (!date) return '';
  const [year, month, day] = date.split('-');
  return `${day}/${month}/${year}`;
}

export function formatDateTimeString(date?: string): string {
  if (!date) return '';
  const [year, month, day] = date.substring(0, 10).split('-');
  const [hour, minutes] = date.substring(11,16).split(':')
  return `${day}/${month}/${year} ${hour}:${minutes}`;
}

export function formatDateTime(date?: Date): string {
  if (!date) return '';
  const dayDate = date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate()
  const month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1
  return `${dayDate}/${month}/${date.getFullYear()}`;
}