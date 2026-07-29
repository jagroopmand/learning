from pprint import pprint
class MergeWindows:

    def __init__(self):
        pass


    def merge(self, windows: list[tuple[float,float]]) -> list[tuple[float, float]]:
       
       if not windows:
           return []

       sorted_windows = sorted(windows, key=lambda w: w[0])
       merged_windows = [sorted_windows[0]]
       for start, end in sorted_windows[1:]:
           prev_start, prev_end = merged_windows[-1]    
           if start < prev_end:
               merged_windows[-1] = (prev_start, max(prev_end, end))
           else:
               merged_windows.append((start,end))


       return merged_windows   

if __name__ == "__main__":
    obj = MergeWindows()   
    pprint(obj.merge([(1,3),(2,4),(6,8),(7,12)]))   


        



