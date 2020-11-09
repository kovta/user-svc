import { mutate } from 'swr';
import { constructUrl } from '.';

export type HttpMethod = 'POST' | 'PUT' | 'DELETE';
export interface MutationParameters<T> {
  method?: HttpMethod;
  path: string;
  resourceId?: string;
  payload: T;
  revalidate?: string[];
}
const useMutation = async <T>({ method = 'POST', path, resourceId, payload, revalidate }: MutationParameters<T>) => {
  const url = constructUrl({ path, resourceId });

  const response = fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const { ok, statusText } = await response;

  console.log('revalidate: ' + ok);
  if (ok && revalidate?.length) {
    revalidate.forEach((path) => mutate(constructUrl({ path: path })));
  }

  return { ok, statusText };
};

export default useMutation;
