import useSwr from 'swr';
import { constructUrl } from '.';
import fetcher from './fetcher';

export interface RequestParameters {
  path: string;
  resourceId?: string;
  query?: string;
}
const useRequest = <T>({ path, resourceId, query }: RequestParameters) => {
  const url = constructUrl({ path, resourceId, query });

  const { data, isValidating, error } = useSwr<T>(url, fetcher);
  return { data, isValidating, error };
};

export default useRequest;
